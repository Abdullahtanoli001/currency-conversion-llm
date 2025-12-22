# AI Currency Converter

Ek zabardast AI-powered currency converter with LangChain & Groq!

## Installation Steps

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment
`.env` file mein apni GROQ_API_KEY daal do:
```
GROQ_API_KEY=your_actual_api_key_here
```

### 3. Run Backend
```bash
python app.py
```
Backend ab `http://localhost:5000` par chal raha hai!

### 4. Run Frontend
Frontend file (`index.html`) ko directly browser mein open kar do ya phir:
```bash
cd frontend
python -m http.server 8000
```
Phir browser mein jao: `http://localhost:8000`

## Features
✨ AI-powered conversions using LangChain
🎨 Beautiful gradient UI
💱 Multiple currencies support
⚡ Real-time conversion
🔄 Swap currencies with animation

## Tech Stack
- **Backend**: Flask + LangChain + Groq
- **Frontend**: HTML + CSS + JavaScript
- **API**: ExchangeRate-API