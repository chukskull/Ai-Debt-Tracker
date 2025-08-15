from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from debt import DebtManager, debt_agent_creator
import os

app = Flask(__name__)
CORS(app)

# Initialize debt manager
debt_manager = DebtManager("debts2.json")

# Initialize AI agent with configurable model
# You can set DEBT_TRACKER_MODEL environment variable to use a different model
print("🚀 Starting Debt Tracker API Server...")
debt_agent = debt_agent_creator()

@app.route('/api/debts', methods=['GET'])
def get_debts():
    """Get all debts"""
    return jsonify(debt_manager.debts)

@app.route('/api/add-debt', methods=['POST'])
def add_debt():
    """Add new debt or add to existing debt"""
    data = request.json
    person = data.get('person')
    amount = float(data.get('amount'))
    description = data.get('description', '')
    
    result = debt_manager.add_to_existing_debt(person, amount, description)
    return jsonify({"message": result})

@app.route('/api/subtract-debt', methods=['POST'])
def subtract_debt():
    """Subtract amount from person's debt (payment)"""
    data = request.json
    person = data.get('person')
    amount = float(data.get('amount'))
    
    result = debt_manager.subtract_debt(person, amount)
    return jsonify({"message": result})

@app.route('/api/mark-paid', methods=['POST'])
def mark_paid():
    """Mark debt as paid"""
    data = request.json
    person = data.get('person')
    debt_id = data.get('debt_id')
    
    result = debt_manager.mark_paid(person, debt_id)
    return jsonify({"message": result})

@app.route('/api/total-debt', methods=['GET'])
def get_total_debt():
    """Get total unpaid debt"""
    total = debt_manager.get_total_debt()
    return jsonify({"total": total})

@app.route('/api/summary', methods=['GET'])
def get_summary():
    """Get debt summary"""
    summary = debt_manager.get_debt_summary()
    return jsonify({"summary": summary})

@app.route('/api/person-balance/<person>', methods=['GET'])
def get_person_balance(person):
    """Get balance for specific person"""
    balance = sum(debt["amount"] for debt in debt_manager.debts 
                 if debt["person"].lower() == person.lower() and debt["status"] == "unpaid")
    return jsonify({"person": person, "balance": balance})

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat with the debt management AI agent"""
    try:
        data = request.json
        message = data.get('message', '')
        
        if not message.strip():
            return jsonify({"response": "Please provide a message."}), 400
        
        response = debt_agent.invoke({"input": message})
        return jsonify({"response": response['output']})
    
    except Exception as e:
        return jsonify({"response": f"Sorry, I encountered an error: {str(e)}"}), 500

@app.route('/api/model-info', methods=['GET'])
def get_model_info():
    """Get current AI model information"""
    try:
        current_model = os.getenv('DEBT_TRACKER_MODEL', 'qwen2:7b')
        
        # Try to get available models from Ollama
        available_models = []
        try:
            import subprocess
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                available_models = [line.split()[0] for line in lines if line.strip()]
        except Exception:
            available_models = ["Unable to fetch available models"]
        
        return jsonify({
            "current_model": current_model,
            "available_models": available_models,
            "instructions": "Set DEBT_TRACKER_MODEL environment variable to change the model"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)