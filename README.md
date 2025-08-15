 # 💰 Debt Tracker AI

I had trouble keeping track of debts. Notes were messy. So I built this — a local debt tracker that works offline, with no external APIs. Your data stays on your machine.

---

## 📌 What It Does

- Chat with it in plain language.
- Track debts in **MAD**.
- See totals and summaries instantly.
- Works on desktop and mobile.
- Stores data locally in `debts.json` (ignored by Git).

---

## ✨ Features

- **AI Chat Interface** — LangChain + Ollama.
- **Modern Web UI** — Next.js + shadcn/ui.
- **Smart Tracking** — Automatic debt summaries.
- **Real-Time Updates** — After every action.
- **Local Storage Only** — No cloud, no API keys.

---

## 🛠 Architecture

### Backend (`/backend`)
- Flask API with CORS.
- LangChain AI agent (Ollama).
- `DebtManager` class handles all logic.
- JSON file for data storage.

### Frontend (`/frontend`)
- Next.js 14 + TypeScript.
- shadcn/ui components.
- Tailwind CSS.
- Vercel AI SDK for chat integration.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- [Ollama](https://ollama.ai/) installed with at least one model.

### Installation

```bash
git clone https://github.com/chukskull/Ai-Debt-Tracker.git
cd Ai-Debt-Tracker
```

Install backend dependencies:
```bash
pip install pandas langchain-ollama langchain flask flask-cors
```

Install an Ollama model:
```bash
# Install Ollama first, then pull a model
ollama pull llama3.2
# or
ollama pull qwen2.5
ollama pull mistral
ollama list
```

Install frontend dependencies:
```bash
cd frontend
npm install --cache /tmp/.npm
```

---

### Running the App

Backend:
```bash
cd backend
python api_server.py
# Runs at http://localhost:8000
```

Frontend (in a new terminal):
```bash
cd frontend
npm run dev
# Runs at http://localhost:3000
```

Open your browser at:  
`http://localhost:3000`

---

## 💬 Example Usage

- `i lent Sarah 500 MAD for lunch`
- `John paid 200 MAD yesterday`
- `mark Sarah as fully paid`
- `how much does everyone owe me?`
- `show all debts`

---

## 🔗 API Endpoints

**AI**
- `POST /api/chat` — Chat with AI.
- `GET /api/model-info` — Get model details.

**Direct**
- `GET /api/debts`
- `POST /api/add-debt`
- `POST /api/subtract-debt`
- `POST /api/mark-paid`
- `GET /api/total-debt`
- `GET /api/summary`
- `GET /api/person-balance/<person>`

---

## 🤖 Model Setup

**Popular Models**
- `llama3.2` — Reliable, balanced.
- `qwen2.5` — Strong multilingual.
- `mistral` — Fast and capable.
- `codellama` — Code-focused.
- `phi3.5` — Lightweight and quick.

**Change Model via Environment Variable**
```bash
export DEBT_TRACKER_MODEL="llama3.2"
python backend/api_server.py
```

Check installed models:
```bash
ollama list
```

---

## 📂 Data Format

```json
{
  "id": 1,
  "person": "John",
  "amount": 500.0,
  "description": "Lunch money",
  "date_added": "2024-08-15T10:00:00.000000",
  "status": "unpaid",
  "date_paid": "2024-08-15T15:30:00.000000"
}
```

Data is stored in `backend/debts.json` and ignored by Git.

---

## 📁 Project Structure

```
/
├── backend/
│   ├── api_server.py
│   ├── debt.py
│   └── debts.json  # Local data
├── frontend/
│   ├── src/app/
│   │   ├── api/chat/
│   │   └── page.tsx
│   └── components/ui/
├── .gitignore
└── README.md
```

---

## ⚙️ Configuration

**Model in Code**
```python
debt_agent = debt_agent_creator(model_name="your-model", temperature=0.7)
```

**Backend Port**
```python
app.run(debug=True, port=8000)
```

**Frontend API URL**
```typescript
const response = await fetch('http://localhost:8000/api/chat', {
```

---

## 🔒 Security

- Local-only storage.
- `.gitignore` protects debt data.
- No external API calls.
- Runs on your hardware.

---

## 🧪 Development Tips

Run CLI version:
```bash
cd backend
python debt.py
```

To add features:
- Backend: edit `debt.py` or `api_server.py`.
- Frontend: update files in `frontend/src/*`.
- AI behavior: change prompt in `debt_agent_creator()`.

---

## 🛠 Troubleshooting

**npm permissions**
```bash
npm install --cache /tmp/.npm
```

**Port in use**
- On macOS, disable AirPlay or change port in `api_server.py`.

**Model not found**
```bash
ollama list
ollama pull llama3.2
export DEBT_TRACKER_MODEL="llama3.2"
```

**Frontend not connecting**
- Ensure backend is running on port `8000`.
- Check API URL in `frontend/src/app/api/chat/route.ts`.

---

## 📜 License

MIT License.

---

## 🤔 Why I Built This

I struggled to track debts in notes and messages. So I made a small tool I can run locally. It’s simple, secure, and keeps my numbers straight.
