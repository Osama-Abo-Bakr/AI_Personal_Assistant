# 🤖 Personalized AI Agent API

![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker)
![CI](https://github.com/Osama-Abo-Bakr/AI_Personal_Assistant/actions/workflows/ci-cd.yml/badge.svg)

A **production-ready FastAPI-based AI Agent** with persistent memory, tool calling, and safe OAuth integration.

---

## ✨ Features

- 🧠 **Persistent Chat Memory** (PostgreSQL + JSONB)
- 🔍 **Web Search** via DuckDuckGo
- ✉️ **Gmail Tools** (OAuth initialized once & cached)
- 📅 **Optional Google Calendar Tools**
- ⚡ **Tool-calling LLM** using LangChain + OpenAI
- 🛡️ Safe startup/shutdown & fail-safe tool isolation
- 🚀 Ready for Railway / Docker deployment

---

## 🧰 Tech Stack

- **Python 3.10+**
- **FastAPI** – API framework
- **LangChain** – Agent & tool orchestration
- **OpenAI** – Chat models
- **PostgreSQL (Railway)** – Persistent memory
- **psycopg2** – Database driver
- **Google Gmail API** – OAuth tools
- **DuckDuckGo Search**
- **Conda / Docker**

---

## 📁 Project Structure

```

.
├── main.py                  # FastAPI entrypoint
├── requirements.txt         # Python dependencies
├── Dockerfile               # Production Docker image
├── .env                     # Environment variables
├── credentials.json         # Google OAuth client credentials
├── token.json               # Gmail OAuth token (auto-generated)
└── src/
├── config.py            # App configuration
├── database/
│   └── db.py            # PostgreSQL chat history logic
└── services/
├── agent.py         # LangChain agent execution
└── tools.py         # Search, Gmail, Calendar tools

````

---

## 🧪 Architecture Highlights

### 🧠 Chat Memory
- Stored as `JSONB` in PostgreSQL
- Loaded on every request
- Automatically updated after each interaction

### 🔧 Tool Calling
- DuckDuckGo search
- Gmail (read / send / summarize)
- Tools are **optional and fail-safe**

### 🔐 Gmail OAuth (One-Time Initialization)
- OAuth runs **only once per app process**
- Gmail tools are cached in memory
- No repeated browser consent prompts
- Safe fallback if OAuth is unavailable

---

## 🚀 Installation (Using Conda)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Osama-Abo-Bakr/AI_Personal_Assistant.git
cd AI_Personal_Assistant
````

### 2️⃣ Create Conda Environment

```bash
conda create -n ai-agent python=3.10 -y
conda activate ai-agent
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Environment Configuration

Create a `.env` file in the project root:

```env
# OpenAI
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx

# PostgreSQL (Railway)
POSTGRES_URL=postgresql://user:password@host:port/database

# API Security
API_TOKEN=123456

# Google OAuth
GCP_CREDENTIALS_PATH=./credentials.json
GMAIL_TOKEN_PATH=token.json
CALENDAR_TOKEN_PATH=calendar_token.json
```

⚠️ **Notes**

* `credentials.json` comes from Google Cloud Console
* `token.json` is generated automatically after OAuth

---

## 🔐 Google OAuth Setup (Gmail)

1. Open **Google Cloud Console**
2. Enable **Gmail API**
3. Create **OAuth Client ID**
4. Download `credentials.json`
5. Place it in the project root

➡️ On the **first API request**, a browser window opens for authorization.

✔ OAuth runs once
✔ Tools cached in memory

---

## ▶️ Run Locally

```bash
python main.py
```

* API: `http://localhost:8000`
* Swagger UI: `http://localhost:8000/docs`

---

## 🐳 Docker (Using Railway PostgreSQL)

> ❌ No PostgreSQL container is required
> ✅ Connects directly to Railway PostgreSQL via `POSTGRES_URL`

### Build Image

```bash
docker build -t ai-agent .
```

### Run Container

```bash
docker run -p 8000:8000 \
  --env-file .env \
  ai-agent
```

### With Google OAuth Credentials (Recommended)

```bash
docker run -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/credentials.json:/app/credentials.json \
  ai-agent
```

---

## 🔌 API Endpoints

### Health Check

```
GET /
```

### Ask the AI Agent

```
POST /query?token=API_TOKEN
```

```json
{
  "user_id": "string",
  "question": "Hello, how can you help me?"
}
```

### Get Chat History

```
GET /chat_history?user_id=string&token=API_TOKEN
```

### Clear Chat History

```
DELETE /chat_history/clear?user_id=string&token=API_TOKEN
```

---

## 🔄 CI/CD (GitHub Actions)

Workflow file:

```
.github/workflows/ci-cd.yml
```

### Pipeline Behavior

**On every push or PR to `main`:**

#### 🧪 Build & Test

* Install dependencies
* Python syntax check (`compileall`)

#### 🐳 Docker Build

* Build Docker image
* Validate Dockerfile
* Ready for Docker Hub / GHCR / Railway

---

## 🚄 Railway Deployment Notes

* No `docker-compose`
* No database image
* Set environment variables in Railway:

  * `POSTGRES_URL`
  * `OPENAI_API_KEY`
  * `API_TOKEN`
  * `GMAIL_TOKEN_PATH`
  * `GCP_CREDENTIALS_PATH`

Railway will:

* Build Docker image
* Run Uvicorn
* Connect to PostgreSQL automatically

---

## 🛡️ Production Notes

* Gmail tools cached once per process
* OAuth isolated from request handling
* PostgreSQL JSONB handled via `psycopg2.extras.Json`
* Safe FastAPI lifespan management

---

## 🔮 Future Enhancements

* Intent-based tool routing
* Background OAuth refresh
* Conversation summarization
* Multi-tenant authentication
* Rate limiting & observability

---

## 👨‍💻 Author

Built with ❤️ as a **production-grade AI assistant backend**.