# Planville Chatbot Backend (FastAPI)

This is the backend engine for the Planville AI Assistant, powered by FastAPI and GPT (RAG), with intent detection, FAQ triggers, and lead capture to Google Sheets.

## Features
- 🤖 /chat endpoint with intelligent fallback
- 📚 FAQ keyword responder
- 🧠 Intent detection: booking, price, timeline
- 📄 Google Sheets integration
- 🌐 Multilingual (DE/EN/ID)

## Start locally
```bash
uvicorn main:app --reload
