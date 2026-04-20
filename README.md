# 📌 AI Customer Support API (FastAPI + LLM + PostgreSQL)

## 🚀 Overview

This project is an AI-powered customer support system built using FastAPI, PostgreSQL, and OpenAI LLMs.
It intelligently handles user queries by combining:

🗄️ SQL database lookup (order details)
📜 Rule-based policy retrieval (vectorless RAG)
🤖 LLM reasoning (OpenAI GPT model)
🧠 Key Features
🔍 Extracts order IDs from natural language queries
🗃️ Fetches order details from PostgreSQL database
📚 Retrieves policy information using lightweight RAG
🤖 Uses LLM (GPT-4o-mini) to generate responses
⚡ FastAPI-based high-performance REST API
🔐 Secure DB connection using SQLAlchemy pooling

## 🏗️ Architecture

User Query
   ↓
FastAPI Endpoint (/ask)
   ↓
Order ID Extraction (Regex)
   ↓
PostgreSQL Lookup (SQLAlchemy)
   ↓
Policy Retrieval (Vectorless RAG)
   ↓
LLM (OpenAI GPT)
   ↓
Final Response

## 📦 Tech Stack

FastAPI

SQLAlchemy

PostgreSQL (Neon / Cloud DB supported)

OpenAI GPT (via LangChain)

Python-dotenv

Uvicorn

## ⚙️ Installation

1. Clone repository
   
git clone https://github.com/your-username/ai-customer-support-api.git
cd ai-customer-support-api

2. Create virtual environment
   
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3. Install dependencies
pip install -r requirements.txt
🔑 Environment Variables

Create a .env file:

DATABASE_URL=postgresql+psycopg2://user:password@host:port/dbname
OPENAI_API_KEY=your_openai_api_key

4. ▶️ Run the application
uvicorn app:app --reload

Server runs at:

http://127.0.0.1:8000
📡 API Endpoint
🔹 POST /ask

Request:

{
  "query": "What is the status of order 12345?"
}

Response:

{
  "answer": "Your order 12345 has been shipped and will be delivered on 2026-04-22.",
  "order_data": {
    "status": "shipped",
    "delivery_date": "2026-04-22",
    "amount": 49.99
  },
  "policy_data": "No policy found."
}

## 🧩 Example Queries

“What is the status of order 12345?”

“Can I return my order?”

“My order is delayed, what can I do?”

“Is order 54321 shipped?”

## 🧠 How It Works

1. Order Processing
Extracts 5-digit order ID using regex

2. Database Layer
Queries PostgreSQL using SQLAlchemy connection pooling
3. Policy Layer (RAG)
Matches keywords like:
return
damaged
delayed
4. LLM Layer
Combines all context
Generates final human-like response
5. ⚡ Performance Features
Connection pooling (fast DB access)
Pre-ping health checks
Async-ready architecture
Minimal latency design

## 🚀 Future Improvements

 LangGraph agent orchestration
 
 CrewAI multi-agent workflow
 
 Vector database integration (Pinecone / Weaviate)
 
 Streaming responses (ChatGPT-like UI)
 
 Authentication layer (JWT)
