"""LLM Agent — generates empathetic mental-health responses.

Priority order:
1. Google Gemini 1.5-Flash with Google Search Grounding (internet access)
2. OpenAI (if API key provided)
3. Local FLAN-T5 model (fallback)

Set GEMINI_API_KEY or OPENAI_API_KEY in backend/.env to enable live responses.
"""

import os
import logging
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

logger = logging.getLogger(__name__)

# Lazy-loaded local model (free LLM) – loaded on first use
_LOCAL_MODEL = None
_LOCAL_TOKENIZER = None

def _load_local_model():
    global _LOCAL_MODEL, _LOCAL_TOKENIZER
    if _LOCAL_MODEL is None:
        logger.info("Loading local LLM (flan-t5-base) for offline generation…")
        _LOCAL_TOKENIZER = AutoTokenizer.from_pretrained("google/flan-t5-base")
        _LOCAL_MODEL = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
    return _LOCAL_MODEL, _LOCAL_TOKENIZER


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

# Treat placeholder values as missing
if OPENAI_API_KEY.lower().startswith("sk-") and "your" in OPENAI_API_KEY.lower():
    OPENAI_API_KEY = ""


SYSTEM_PROMPT = """You are Antarman, a compassionate and empathetic AI mental‑health companion.
Your role is to:
- Listen carefully and respond with warmth and empathy
- Ask gentle follow‑up questions to better understand the person's feelings
- Offer concrete coping strategies (breathing exercises, grounding techniques, resources) when appropriate
- Never diagnose or prescribe — always encourage professional help when needed
- Keep responses concise but informative (3‑5 sentences) and conversational

Always answer in clear, simple English. The user's message has already been translated to English for you.
"""


def get_llm_response(english_text: str, conversation_history: list[dict] | None = None) -> str:
    """Generate an empathetic response to *english_text*.

    Args:
        english_text:         The user's message already translated to English.
        conversation_history: Optional list of prior messages in OpenAI format
                              [{"role": "user"|"assistant", "content": "..."}]

    Returns:
        An English response string.
    """

    # Try Gemini with Google Search Grounding first
    if GEMINI_API_KEY:
        try:
            from google import genai
            from google.genai import types

            logger.info("Using Gemini 1.5-Flash with Google Search Grounding…")
            client = genai.Client(api_key=GEMINI_API_KEY)

            # Build conversation context
            conversation_str = ""
            if conversation_history:
                for msg in conversation_history[-4:]:  # Last 4 turns for context
                    conversation_str += f"{msg['role'].upper()}: {msg['content']}\n"

            full_prompt = f"{SYSTEM_PROMPT}\n\nContext:\n{conversation_str}\nUser: {english_text}\nAssistant:"

            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())]
                )
            )
            return response.text.strip()

        except Exception as exc:
            logger.error("Gemini call failed: %s", exc)

    # Try OpenAI
    if OPENAI_API_KEY:
        try:
            from openai import OpenAI
            logger.info("Falling back to OpenAI…")
            client = OpenAI(api_key=OPENAI_API_KEY)

            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            if conversation_history:
                messages.extend(conversation_history)
            messages.append({"role": "user", "content": english_text})

            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=300,
                temperature=0.8,
            )
            return completion.choices[0].message.content.strip()
        except Exception as exc:
            logger.error("OpenAI call failed: %s", exc)

    # Fallback to local model
    logger.info("Falling back to local free LLM (no internet access).")
    model, tokenizer = _load_local_model()
    prompt = f"{SYSTEM_PROMPT}\nUser: {english_text}\nAssistant:".strip()
    inputs = tokenizer(prompt, return_tensors="pt")
    output_ids = model.generate(**inputs, max_length=200, temperature=0.7)
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    if response.lower().startswith("assistant:"):
        response = response[len("assistant:"):].strip()
    return response
