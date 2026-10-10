# PDF Chatbot (RAG)

A web app that answers questions about an uploaded PDF using Retrieval-Augmented Generation.

## How it works
1. The PDF text is split into overlapping chunks
2. Chunks are embedded and stored in Chroma, a vector database
3. For each question, the 4 most similar chunks are retrieved
4. Gemini answers using only those chunks

## Tech stack
Python, Flask, ChromaDB, pypdf, Google Gemini API, Bootstrap

## Setup (Windows PowerShell)
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    $env:GEMINI_API_KEY="your_key_here"
    python app.py

Open http://127.0.0.1:5000, upload a text-based PDF, and ask questions.

## Notes
- Get a free API key from Google AI Studio
- Scanned PDFs are not supported
- Never commit your API key
Practice edit
