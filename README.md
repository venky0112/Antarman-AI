# Antarman-AI

Antarman AI — Mental health AI companion for Indian languages powered by Google Gemini 1.5-Flash with internet access for up-to-date crisis resources, real-time crisis detection (DistilBERT + Regex fallback).

## Overview

Antarman AI is a mental health artificial intelligence system specifically designed for Indian languages. The system uses Google Gemini 1.5-Flash (with internet access) for empathetic responses and integrates real-time crisis detection to identify high-risk situations.

## Features

### Internet-Connected Intelligence
- Uses Google Gemini 1.5-Flash with Google Search Grounding
- Access to current mental health resources and crisis helplines
- Always up-to-date with latest mental health information

### Indian Languages
- Support for Hindi, Tamil, Telugu, Kannada, Bengali, Gujarati, Malayalam, Punjabi, and more
- Automatic language detection with multi-language support
- Culturally tailored responses for Indian language speakers

### Real-Time Crisis Detection
- Real-time mental health crisis identification
- Uses DistilBERT model for crisis assessment
- Regex fallback patterns for keyword-based detection
- Immediate crisis alerts with emergency hotlines

### Empathetic & Safe
- System prompt ensures compassionate, empathetic responses
- Never diagnoses or prescribes — encourages professional help
- Offers concrete coping strategies (breathing exercises, grounding techniques)
- Multi-turn conversation support for context-aware responses

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Internet connection (for Gemini API)

### Setup

1. **Clone/Download the repository:**
   ```bash
   cd c:\Users\Venkatesh.Tomar02\Downloads\Antarman-AI
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Configure Gemini API Key:**
   - Get your free Gemini API key from: [ai.google.dev](https://ai.google.dev/metrics/explorer)
   - Open `backend/.env` and add:
     ```
     GEMINI_API_KEY=your_key_here
     ```

5. **Verify the setup:**
   ```bash
   python test_gemini.py
   ```

## Usage

### Run the Interactive Chat
```bash
python main.py
```

Example interaction:
```
You: I'm feeling anxious
  [Language detected: en]
  [Crisis Status: ✓ Safe]

Antarman: I'm sorry you're feeling anxious. That's a real and valid experience. 
Let's work through this together. Can you tell me what's triggering your anxiety? 
Sometimes just naming the source helps us understand it better.
```

### Features
- Type `quit` or `exit` to end the conversation
- Automatic language detection for Hindi, Tamil, Telugu, and more
- Real-time crisis alerts with emergency helplines
- Multi-turn conversation support for context-aware responses

## Troubleshooting

See [GEMINI_FIXES.md](GEMINI_FIXES.md) for detailed debugging information and common issues.



## Contributing


