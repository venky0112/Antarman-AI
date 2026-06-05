import sys
import os
import logging
import io

# Force Windows console to output UTF-8 so printing Hindi/non-ASCII characters won't crash
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configure basic logging — set to ERROR to silence network warnings
logging.basicConfig(level=logging.ERROR)

# Load environment variables
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
load_dotenv(dotenv_path=env_path)

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.crisis_detector import predict_crisis
from backend.translator import translate_to_english, translate_from_english
from backend.llm_agent import get_llm_response


def detect_language(text: str) -> str:
    """Detect the language of *text* using deep-translator's built-in detector.
    Returns an ISO 639-1 language code (e.g. 'hi', 'ta', 'en').
    Falls back to 'en' if detection fails.
    """
    try:
        from deep_translator import single_detection
        lang = single_detection(text, api_key=None)
        return lang if lang else "en"
    except Exception:
        pass

    # Lightweight script-based heuristic (no network needed)
    for ch in text:
        cp = ord(ch)
        if 0x0900 <= cp <= 0x097F:   # Devanagari  → Hindi / Marathi
            return "hi"
        if 0x0B80 <= cp <= 0x0BFF:   # Tamil
            return "ta"
        if 0x0C00 <= cp <= 0x0C7F:   # Telugu
            return "te"
        if 0x0980 <= cp <= 0x09FF:   # Bengali
            return "bn"
        if 0x0A80 <= cp <= 0x0AFF:   # Gujarati
            return "gu"
        if 0x0A00 <= cp <= 0x0A7F:   # Punjabi (Gurmukhi)
            return "pa"
        if 0x0D00 <= cp <= 0x0D7F:   # Malayalam
            return "ml"
        if 0x0C80 <= cp <= 0x0CFF:   # Kannada
            return "kn"
    return "en"


def main():
    print("=" * 55)
    print("   Antarman AI — Mental Health Companion")
    print("=" * 55)
    print("Supports: English, Hindi, Tamil, Telugu, Bengali,")
    print("          Gujarati, Kannada, Malayalam, Punjabi, ...")
    print("Type 'quit' to exit.\n")

    conversation_history: list[dict] = []

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['quit', 'exit']:
                print("Take care. Goodbye! 🙏")
                break

            # ── Step 1: Detect Language ────────────────────────────────────
            src_lang = detect_language(user_input)
            if src_lang != "en":
                print(f"  [Language detected: {src_lang}]")

            # ── Step 2: Crisis Detection (on original text) ────────────────
            is_crisis = predict_crisis(user_input)
            if is_crisis:
                print("\n⚠️  CRISIS ALERT: This message indicates potential self-harm or crisis.")
                print("   Please contact a helpline immediately:")
                print("   • iCall (India): 9152987821")
                print("   • Vandrevala Foundation: 1860-2662-345 (24x7)")
                # Still continue to give a supportive response

            # ── Step 3: Translate to English ───────────────────────────────
            english_text = translate_to_english(user_input, src_lang)
            if src_lang != "en":
                print(f"  [Translated → English]: {english_text}")

            # ── Step 4: LLM generates response in English ──────────────────
            english_response = get_llm_response(english_text, conversation_history)

            # Update conversation history for multi-turn context
            conversation_history.append({"role": "user",    "content": english_text})
            conversation_history.append({"role": "assistant", "content": english_response})
            # Keep last 10 turns to avoid token overflow
            if len(conversation_history) > 20:
                conversation_history = conversation_history[-20:]

            # ── Step 5: Translate response back to user's language ─────────
            final_response = translate_from_english(english_response, src_lang)

            print(f"\nAntarman: {final_response}\n")

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
