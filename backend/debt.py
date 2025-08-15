import pandas as pd
import json
from datetime import datetime
from typing import List, Dict, Any
from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import BaseTool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
import os

class DebtManager:
    def __init__(self, file_path: str = "debts.json"):
        self.file_path = file_path
        self.debts = self.load_debts()
    
    def load_debts(self) -> List[Dict]:
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                return json.load(f)
        return []
    
    def save_debts(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.debts, f, indent=2)
    
    def add_debt(self, person: str, amount: float, description: str = ""):
        debt = {
            "id": len(self.debts) + 1,
            "person": person,
            "amount": amount,
            "description": description,
            "date_added": datetime.now().isoformat(),
            "status": "unpaid"
        }
        self.debts.append(debt)
        self.save_debts()
        return f"Added debt: ${amount} to {person}"

    def subtract_debt(self, person: str, amount: float, description: str = ""):
        """Subtract amount from person's existing debt"""
        found = False
        for debt in self.debts:
            if debt["person"].lower() == person.lower() and debt["status"] == "unpaid":
                debt["amount"] -= amount
                debt["description"] += f" | Payment: ${amount}"
                found = True
                break
        
        if not found:
            return f"No unpaid debt found for {person}"
        
        self.save_debts()
        return f"Subtracted ${amount} from {person}'s debt"
    
    def add_to_existing_debt(self, person: str, amount: float, description: str = ""):
        """Add amount to person's existing debt"""
        found = False
        for debt in self.debts:
            if debt["person"].lower() == person.lower() and debt["status"] == "unpaid":
                debt["amount"] += amount
                debt["description"] += f" | Additional: ${amount}"
                found = True
                break
        
        if not found:
            # Create new debt if person doesn't exist
            return self.add_debt(person, amount, description)
        
        self.save_debts()
        return f"Added ${amount} to {person}'s existing debt"
        
    
    def mark_paid(self, person: str = None, debt_id: int = None):
        if debt_id:
            for debt in self.debts:
                if debt["id"] == debt_id and debt["status"] == "unpaid":
                    debt["status"] = "paid"
                    debt["date_paid"] = datetime.now().isoformat()
                    self.save_debts()
                    return f"Marked debt ID {debt_id} as paid"
        elif person:
            for debt in self.debts:
                if debt["person"].lower() == person.lower() and debt["status"] == "unpaid":
                    debt["status"] = "paid"
                    debt["date_paid"] = datetime.now().isoformat()
                    self.save_debts()
                    return f"Marked debt to {person} as paid"
        return "Debt not found or already paid"
    
    def get_total_debt(self) -> float:
        return sum(debt["amount"] for debt in self.debts if debt["status"] == "unpaid")
    
    def get_debt_summary(self) -> str:
        if not self.debts:
            return "No debts recorded"
        
        total_unpaid = self.get_total_debt()
        total_paid = sum(debt["amount"] for debt in self.debts if debt["status"] == "paid")
        
        summary = f"DEBT SUMMARY:\n"
        summary += f"Total unpaid: ${total_unpaid:.2f}\n"
        summary += f"Total paid: ${total_paid:.2f}\n\n"
        
        # Group by person
        by_person = {}
        for debt in self.debts:
            if debt["status"] == "unpaid":
                person = debt["person"]
                if person not in by_person:
                    by_person[person] = 0
                by_person[person] += debt["amount"]
        
        if by_person:
            summary += "UNPAID DEBTS BY PERSON:\n"
            for person, amount in by_person.items():
                summary += f"- {person}: ${amount:.2f}\n"
        
        return summary
    
    def list_all_debts(self) -> str:
        if not self.debts:
            return "No debts recorded"
        
        result = "ALL DEBTS:\n"
        for debt in self.debts:
            status_icon = "✓" if debt["status"] == "paid" else "✗"
            result += f"{status_icon} ID:{debt['id']} - {debt['person']}: ${debt['amount']:.2f}"
            if debt['description']:
                result += f" ({debt['description']})"
            result += f" - {debt['date_added'][:10]}\n"
        
        return result

debt_manager = DebtManager("debts.json")


@tool
def add_debt_tool(person: str, amount: float, description: str = "") -> str:
    """Add amount to existing debt or create new debt if person doesn't exist."""
    return debt_manager.add_to_existing_debt(person, amount, description)

@tool
def substract_debt_tool(person: str, amount: float, description: str = "") -> str:
    """Subtract amount from person's existing debt when they pay you back."""
    return debt_manager.subtract_debt(person, amount, description)

@tool
def mark_debt_paid_tool(person: str = None, debt_id: int = None) -> str:
    """Mark a debt as paid. You can specify either person name or debt ID."""
    return debt_manager.mark_paid(person, debt_id)

@tool
def get_total_debt_tool() -> str:
    """Get the total amount of unpaid debt."""
    total = debt_manager.get_total_debt()
    return f"Total unpaid debt: ${total:.2f}"

@tool
def get_debt_summary_tool() -> str:
    """Get a comprehensive summary of all debts, organized by person."""
    return debt_manager.get_debt_summary()

@tool
def list_all_debts_tool() -> str:
    """List all debts (both paid and unpaid) with details."""
    return debt_manager.list_all_debts()

@tool
def get_person_balance_tool(person: str) -> str:
    """Get the current debt balance for a specific person."""
    balance = sum(debt["amount"] for debt in debt_manager.debts 
                 if debt["person"].lower() == person.lower() and debt["status"] == "unpaid")
    return f"{person}'s current debt: ${balance:.2f}"


def debt_agent_creator(model_name: str = None, temperature: float = 0.7):
    """
    Create a debt management agent with configurable LLM model.
    
    Args:
        model_name (str): Name of the Ollama model to use. If None, tries environment variable or defaults.
        temperature (float): Model temperature for response creativity (0.0-1.0)
    
    Supported models include:
        - llama3.2, llama3.1, llama3, llama2
        - qwen2.5, qwen2, qwen
        - mistral, mixtral
        - codellama, deepseek-coder
        - gemma2, gemma
        - phi3, phi3.5
        - And any other model available in your Ollama installation
    """
    # Model selection priority: parameter -> environment variable -> default
    if model_name is None:
        model_name = os.getenv('DEBT_TRACKER_MODEL', 'qwen2:7b')
    
    print(f"🤖 Initializing Debt Tracker AI with model: {model_name}")
    print(f"🌡️  Temperature: {temperature}")
    
    try:
        model = ChatOllama(
            model=model_name,
            temperature=temperature,
            # Add timeout for better error handling
            timeout=30
        )
        
        # Test the model connection
        _ = model.invoke("Hello")
        print(f"✅ Model {model_name} is ready!")
        
    except Exception as e:
        print(f"❌ Error initializing model {model_name}: {e}")
        print("💡 Available models in Ollama:")
        try:
            import subprocess
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            print(result.stdout)
        except:
            print("   Run 'ollama list' to see available models")
        raise e
    tools = [
        add_debt_tool,
        substract_debt_tool,
        mark_debt_paid_tool,
        get_total_debt_tool,
        get_debt_summary_tool,
        list_all_debts_tool,
        get_person_balance_tool
    ]
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful debt management assistant. You help track money in Dirham (MAD) that people owe.
        
        You can:
        - Add new debts when someone owes money
        - Substract debts when someone give money
        - Mark debts as paid
        - Show debt summaries and totals
        - List all debts
        
        IMPORTANT: After every action or query, you MUST automatically call the get_debt_summary_tool to show the current status of all people who owe money. This should happen in EVERY response, even for simple questions.
        
        Be conversational and helpful. Parse natural language requests like:
        - "I lent Sarah 500MAD for lunch"
        - "John gave me 20MAD yesterday substract it from his total debt"
        - "Sarah paid me back"
        - "How much does everyone owe me?"
        - "Show me all my debts"
        
        Always be clear about what action you're taking and then show the updated debt summary."""),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    agent = create_tool_calling_agent(model, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor


def main():
    agent = debt_agent_creator()
    while True:
        try:
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            response = agent.invoke({"input": user_input})
            print(f"\n🤖 Agent: {response['output']}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == '__main__':
    main()

