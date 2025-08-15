# 💰 Debt Tracker AI

A modern debt management application with AI-powered natural language interface built with Python backend and React frontend.

## 🌟 Features

- **🤖 AI-Powered Chat Interface** - Natural language debt management using LangChain and Ollama
- **💬 Modern Web UI** - Beautiful chat interface built with Next.js, React, and shadcn/ui components
- **📊 Smart Debt Tracking** - Track debts in MAD (Moroccan Dirham) with automatic summaries
- **🔄 Real-time Updates** - Instant debt status updates after every operation
- **📱 Responsive Design** - Works seamlessly on desktop and mobile devices
- **🛡️ Secure Data Storage** - Local JSON-based storage with .gitignore protection

## 🏗️ Architecture

### Backend (`/backend/`)
- **Flask API Server** - RESTful API with CORS support
- **LangChain AI Agent** - Natural language processing with Ollama qwen2:7b model
- **DebtManager Class** - Core business logic for debt operations
- **JSON Data Storage** - Simple, reliable local data persistence

### Frontend (`/frontend/`)
- **Next.js 14** - React framework with TypeScript
- **shadcn/ui Components** - Beautiful, accessible UI components
- **Tailwind CSS** - Utility-first CSS framework
- **Vercel AI SDK** - Seamless AI chat integration

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- [Ollama](https://ollama.ai/) with any compatible model (see supported models below)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/chukskull/Ai-Debt-Tracker.git
cd Ai-Debt-Tracker
```

2. **Install Python dependencies**
```bash
pip install pandas langchain-ollama langchain flask flask-cors
```

3. **Install Ollama and pull a model**
```bash
# Install Ollama (visit https://ollama.ai for instructions)

# Choose one or more models to install:
ollama pull llama3.2        # Latest Llama model (recommended)
ollama pull qwen2.5         # Latest Qwen model  
ollama pull mistral         # Mistral 7B
ollama pull codellama       # Code-specialized model
ollama pull gemma2          # Google's Gemma 2
ollama pull phi3.5          # Microsoft's Phi-3.5

# Or any other model available in Ollama
ollama list                 # See available models
```

4. **Install frontend dependencies**
```bash
cd frontend
npm install --cache /tmp/.npm  # Use temp cache if you have npm permission issues
```

### Running the Application

1. **Start the Backend Server**
```bash
cd backend
python api_server.py
```
Server runs on `http://localhost:8000`

2. **Start the Frontend (new terminal)**
```bash
cd frontend
npm run dev
```
Frontend runs on `http://localhost:3000`

3. **Open your browser** and navigate to `http://localhost:3000`

## 🤖 AI Model Configuration

The Debt Tracker AI supports **any local LLM** running through Ollama! You can easily switch between different models.

### Supported Models

#### 🦙 **Meta Llama Family**
- `llama3.2` (Latest, recommended)
- `llama3.1`, `llama3`, `llama2`
- `codellama` (Code-specialized)

#### 🧠 **Qwen Family**  
- `qwen2.5` (Latest)
- `qwen2:7b`, `qwen2:1.5b`
- `qwen:14b`, `qwen:7b`

#### 🌟 **Other Popular Models**
- `mistral`, `mixtral` (Mistral AI)
- `gemma2`, `gemma` (Google)
- `phi3.5`, `phi3` (Microsoft)
- `deepseek-coder` (Coding specialist)
- `neural-chat` (Intel)
- And **any other model** available in Ollama!

### Changing Models

#### Method 1: Environment Variable
```bash
# Set your preferred model
export DEBT_TRACKER_MODEL="llama3.2"
cd backend && python api_server.py

# Or in one line
DEBT_TRACKER_MODEL="mistral" python api_server.py
```

#### Method 2: Check Available Models
```bash
# See what models you have installed
ollama list

# Check current model via API
curl http://localhost:8000/api/model-info
```

#### Method 3: Model Performance Comparison
Different models have different strengths:
- **llama3.2**: Best overall performance, great reasoning
- **qwen2.5**: Excellent multilingual support, fast
- **mistral**: Good balance of speed and capability  
- **codellama**: Better for technical/structured responses
- **phi3.5**: Lightweight, fast responses

### Model Requirements
- **RAM**: 7B models need ~8GB RAM, 13B+ models need ~16GB RAM
- **Speed**: Smaller models (1.5B-7B) respond faster
- **Quality**: Larger models typically give better responses

## 💬 Usage Examples

Chat with the AI assistant using natural language:

- **Add a debt**: "I lent Sarah 500 MAD for lunch"
- **Record payment**: "John gave me 200 MAD yesterday, subtract it from his debt"
- **Mark as paid**: "Sarah paid me back completely"
- **Check totals**: "How much does everyone owe me?"
- **View all debts**: "Show me all my debts"

The AI automatically shows updated debt summaries after every operation!

## 📚 API Endpoints

### AI Endpoints
- `POST /api/chat` - Interact with the AI agent
- `GET /api/model-info` - Get current model info and available models

### Direct API Endpoints
- `GET /api/debts` - List all debts
- `POST /api/add-debt` - Add or increase debt amount
- `POST /api/subtract-debt` - Record debt payment
- `POST /api/mark-paid` - Mark debt as fully paid
- `GET /api/total-debt` - Get total unpaid amount
- `GET /api/summary` - Get formatted debt summary
- `GET /api/person-balance/<person>` - Get specific person's balance

## 🗂️ Project Structure

```
/
├── backend/
│   ├── api_server.py    # Flask API server
│   ├── debt.py          # Core debt management logic and AI agent
│   └── debts.json       # Data storage (ignored by Git)
├── frontend/            # Next.js React application
│   ├── src/app/
│   │   ├── api/chat/    # API route handlers
│   │   └── page.tsx     # Main chat interface
│   └── components/ui/   # shadcn/ui components
├── .gitignore          # Protects sensitive debt data
└── README.md           # This file
```

## 🛠️ Development

### Running CLI Interface (Alternative)
```bash
cd backend
python debt.py
```

### Adding New Features

1. **Backend**: Modify `debt.py` for new tools or `api_server.py` for new endpoints
2. **Frontend**: Update components in `frontend/src/` and add new UI elements
3. **AI Behavior**: Modify the system prompt in `debt_agent_creator()` function

### Data Format

Each debt entry contains:
```json
{
  "id": 1,
  "person": "John",
  "amount": 500.0,
  "description": "Lunch money",
  "date_added": "2024-08-15T10:00:00.000000",
  "status": "unpaid",
  "date_paid": "2024-08-15T15:30:00.000000" // if paid
}
```

## 🔧 Configuration

### AI Model Selection
Set your preferred model using environment variable:
```bash
export DEBT_TRACKER_MODEL="llama3.2"        # Meta Llama 3.2
export DEBT_TRACKER_MODEL="qwen2.5"         # Qwen 2.5
export DEBT_TRACKER_MODEL="mistral"         # Mistral 7B
export DEBT_TRACKER_MODEL="codellama"       # CodeLlama
```

Or programmatically in `backend/api_server.py`:
```python
debt_agent = debt_agent_creator(model_name="your-model", temperature=0.7)
```

### Backend Port
Default: `8000`. Change in `backend/api_server.py`:
```python
app.run(debug=True, port=YOUR_PORT)
```

### Frontend API URL
Update in `frontend/src/app/api/chat/route.ts`:
```typescript
const response = await fetch('http://localhost:YOUR_PORT/api/chat', {
```

## 🛡️ Security & Privacy

- **Local Data Storage**: All debt data stays on your machine
- **Git Protection**: `.gitignore` prevents accidental commits of sensitive data
- **No External APIs**: Debt data never leaves your system
- **Local AI**: Uses locally-run Ollama model for privacy

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [shadcn/ui](https://ui.shadcn.com/) - Beautiful UI components
- [LangChain](https://langchain.com/) - AI framework
- [Ollama](https://ollama.ai/) - Local AI model serving
- [Next.js](https://nextjs.org/) - React framework
- [Flask](https://flask.palletsprojects.com/) - Python web framework

## ⚠️ Troubleshooting

### Common Issues

**npm permission errors:**
```bash
npm install --cache /tmp/.npm
```

**Port 5000 already in use:**
- macOS: Disable AirPlay Receiver in System Preferences
- Or: Change port in `api_server.py`

**Ollama model not found:**
```bash
# Check available models
ollama list

# Pull your preferred model
ollama pull llama3.2      # or any other model
ollama pull qwen2.5
ollama pull mistral

# Set the model
export DEBT_TRACKER_MODEL="llama3.2"
```

**Frontend not connecting to backend:**
- Ensure backend is running on port 8000
- Check API URL in `frontend/src/app/api/chat/route.ts`

---

💡 **Need help?** Open an issue on GitHub for support and feature requests.