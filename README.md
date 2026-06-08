# Antarman AI

**An open-source mental health AI assistant for Indian languages — built for privacy, accessibility, and cultural context.**

> Status: Early Prototype — Active Development
>
> Note: Due to technical inconsistencies in the initial setup, development has been migrated from the `main` branch to a new branch called `final-clean`, which is now the primary working branch. All active development, contributions, and pull requests should target `final-clean`.

---

## Overview

Mental health resources in India are scarce, stigmatized, and rarely available in regional languages. Antarman AI is an attempt to address this gap by building a conversational AI companion that can communicate in Indian languages, detect distress signals in real time, and respond with empathy grounded in clinical context.

This project is in its early prototype stage. The current codebase establishes the foundational pipeline — language detection, crisis screening, translation, and LLM-based response generation — as a working CLI application, with the intent to iterate toward a more robust, evaluated, and deployable system.

---

## Current State

The `final-clean` branch contains a working CLI prototype with the following components functional end-to-end:

- Language detection on raw user input using `langdetect`
- Real-time crisis and suicidality screening on the original user message, before any translation
- Input translation from Indian languages to English using Google Translate via `deep-translator`
- Conversational response generation via Google Gemini 2.5 Flash with multi-turn conversation context (last 10 turns retained)
- Response translation back to the user's detected language
- Windows UTF-8 console compatibility for non-ASCII Indian language output

---

## Architecture

The current pipeline runs as a command-line loop in the following order:

```
User Input (any Indian language)
        |
        v
Language Detection (langdetect)
        |
        v
Crisis Detection on raw input (HuggingFace classifier -> regex fallback)
        |
        v
Translation to English (deep-translator / Google Translate)
        |
        v
LLM Response Generation (Google Gemini 2.5 Flash)
        |
        v
Translation back to User's Language (deep-translator)
        |
        v
Response printed to console
```

Crisis detection deliberately runs on the original untranslated text to avoid losing signal during translation. Components are modular and designed to be swapped or upgraded independently as the project matures.

---

## Technology Stack

The stack below reflects what is currently in use. Some choices are provisional and may change as development progresses and constraints become clearer.

| Component | Current Implementation | Notes |
|---|---|---|
| Entry Point | CLI (main.py) | Interactive terminal loop |
| LLM | Google Gemini 2.5 Flash | Via `google-generativeai` SDK |
| Translation | deep-translator (Google Translate) | No API key required |
| Language Detection | langdetect | Lightweight, offline |
| Crisis Detection (primary) | HuggingFace `transformers` pipeline | Model: `cogint/suicidality-detection` |
| Crisis Detection (fallback) | Regex pattern matching | Activates if model load fails |
| Environment Config | python-dotenv | Loads from `backend/.env` |

---

## Project Structure

```
Antarman-AI/                    (primary branch: final-clean)
├── backend/
│   ├── __init__.py
│   ├── llm_agent.py            # Gemini-based response generation with multi-turn context
│   ├── translator.py           # Bidirectional translation pipeline with offline fallback
│   ├── crisis_detector.py      # Crisis classification with regex fallback
│   ├── .env                    # Local secrets (not committed)
│   └── .env.example            # Environment variable template
├── Docs/                       # Research notes, architecture decisions
├── scratch/                    # Experiments and early prototypes
├── main.py                     # CLI entry point — run this to start the assistant
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- A Google Gemini API key — obtain one at [https://ai.google.dev](https://ai.google.dev)
- (Optional) A HuggingFace token for accessing the primary crisis detection model

### Installation

```bash
# Clone the repository
git clone https://github.com/venky0112/Antarman-AI.git
cd Antarman-AI

# Switch to the active development branch
git checkout final-clean

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Copy the environment template and fill in your keys:

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env`:

```env
GEMINI_API_KEY="your_gemini_api_key_here"
HF_TOKEN="your_huggingface_token_here"         # Optional — falls back to public model
CRISIS_MODEL_ID="cogint/suicidality-detection" # Override to use a different model
```

### Running the Assistant

```bash
python main.py
```

This starts an interactive CLI session. Type your message in any supported language and press Enter. Type `quit` or `exit` to end the session.

---

## Supported Languages

The translation layer supports all languages available through Google Translate. The following have been explicitly handled in the codebase:

- Hindi (`hi`)
- Tamil (`ta`)
- Telugu (`te`)
- Bengali (`bn`)
- Marathi (`mr`)
- Gujarati (`gu`)
- Kannada (`kn`)
- Malayalam (`ml`)

An offline static fallback dictionary is included for a subset of common phrases in Hindi, Tamil, Telugu, and Bengali, used when network access is unavailable.

---

## Roadmap

- [x] Core pipeline: detect language -> screen for crisis -> translate -> generate -> translate back
- [x] Google Gemini integration with multi-turn conversation context
- [x] Crisis detection with HuggingFace model and regex fallback
- [x] Configurable environment via `backend/.env`
- [x] Windows UTF-8 console support for Indian language output
- [ ] Finalize and evaluate model choices for LLM and crisis detection
- [ ] Add RAG pipeline over mental health knowledge sources
- [ ] REST API layer (FastAPI) to expose the pipeline as a service
- [ ] Build a basic chat UI (web or mobile)
- [ ] Evaluate translation quality across all supported languages
- [ ] Safety benchmarking and red-teaming
- [ ] Expand offline fallback dictionary coverage
- [ ] Community testing and feedback iteration

---

## Contributing

This project is in early development. Contributions, ideas, and feedback are welcome. Please open an issue before submitting a pull request so the approach can be discussed. Target all pull requests at the `final-clean` branch.

---

## Disclaimer

Antarman AI is a research prototype. It is not a substitute for professional mental health care. The responses generated by this system have not been clinically validated. If you or someone you know is in crisis, please contact a licensed mental health professional or a crisis helpline such as iCall (India): 9152987821.
