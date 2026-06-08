import sys
import os
import logging
import io
from langdetect import detect

# Force Windows console to output UTF-8 so printing Hindi/non-ASCII characters won't crash
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configure basic logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
load_dotenv(dotenv_path=env_path)

# Add backend to path so we can import its modules dynamically (optional now)
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.crisis_detector import predict_crisis
from backend.translator import translate_to_english, translate_from_english
from backend.llm_agent import get_llm_response

def detect_language(text: str) -> str:
    """Detect language code (ISO 639‑1) using langdetect.
    Returns 'en' if detection fails.
    """
    try:
        # langdetect may raise exception for empty or ambiguous text
        lang = detect(text)
        return lang
    except Exception:
        return "en"


def main():
    print("=" * 55)
    print("   Antarman AI — Mental Health Companion")
    print("=" * 55)
    print("Supports: English, Hindi, Tamil, Telugu, Bengali,")
    print("          Gujarati, Kannada, Malayalam, Punjabi, ...")
    print("Type 'quit' to exit.\n")

    # Check if Gemini API key is configured
    if not os.getenv("GEMINI_API_KEY", "").strip():
        print("⚠️  WARNING: GEMINI_API_KEY not set in backend/.env")
        print("   Get your free API key from: https://ai.google.dev/metrics/explorer")
        print("   Add it to backend/.env as: GEMINI_API_KEY=your_key_here\n")

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
                print("  [Crisis Status: ⚠️ CRITICAL]")
                print("\n⚠️  CRISIS ALERT: This message indicates potential self-harm or crisis.")
                print("   Please contact a helpline immediately:")
                print("   • iCall (India): 9152987821")
                print("   • Vandrevala Foundation: 1860-2662-345 (24x7)\n")
            else:
                print("  [Crisis Status: ✓ Safe]")

            # ── Step 3: Translate to English ───────────────────────────────
            english_text = translate_to_english(user_input, src_lang)
            if src_lang != "en":
                print(f"  [Translated → English]: {english_text}")

            # ── Step 4: LLM generates response in English ──────────────────
            try:
                english_response = get_llm_response(english_text, conversation_history)
            except RuntimeError as e:
                print(f"\n❌ Error: {e}")
                print("   Please ensure GEMINI_API_KEY is set correctly in backend/.env\n")
                continue

            # Update conversation history for multi-turn context
            conversation_history.append({"role": "user",    "content": english_text})
            conversation_history.append({"role": "assistant", "content": english_response})
            # Keep last 10 turns to avoid token overflow
            if len(conversation_history) > 20:
                conversation_history = conversation_history[-20:]

            # ── Step 5: Translate response back to user's language ─────────
            if src_lang != "en":
                final_response = translate_from_english(english_response, src_lang)
                print(f"\nAntarman ({src_lang.upper()}): {final_response}\n")
            else:
                print(f"\nAntarman: {english_response}\n")

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
