"""LLM Agent — generates empathetic mental-health responses via OpenAI API.

The agent always receives text in English (translated upstream by translator.py)
and always returns a response in English (which translator.py converts back to
the user's language downstream).

Set OPENAI_API_KEY in backend/.env to enable live responses.
If the key is missing or the call fails, a graceful fallback reply is returned.
"""

import os
import logging

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

SYSTEM_PROMPT = """You are Antarman, a compassionate and empathetic AI mental-health companion.
Your role is to:
- Listen carefully and respond with warmth and empathy
- Ask gentle follow-up questions to better understand the person's feelings
- Offer helpful coping strategies when appropriate
- Never diagnose or prescribe — always encourage professional help when needed
- Keep responses concise (2-4 sentences) and conversational

Always respond in clear, simple English. The user's message has already been 
translated to English for you.
"""

FALLBACK_REPLIES = [
    "I hear you, and I'm here to listen. Could you tell me more about how you're feeling right now?",
    "Thank you for sharing that with me. It sounds like you're going through a difficult time — you're not alone.",
    "I understand. Your feelings are valid. What's been weighing on your mind the most lately?",
    "I'm glad you reached out. Can you share a bit more so I can better support you?",
]

_fallback_index = 0


def get_llm_response(english_text: str, conversation_history: list[dict] | None = None) -> str:
    """Generate an empathetic response to *english_text*.

    Args:
        english_text:         The user's message already translated to English.
        conversation_history: Optional list of prior messages in OpenAI format
                              [{"role": "user"|"assistant", "content": "..."}]

    Returns:
        An English response string.
    """
    global _fallback_index

    if not OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY not set — using fallback reply.")
        reply = FALLBACK_REPLIES[_fallback_index % len(FALLBACK_REPLIES)]
        _fallback_index += 1
        return reply

    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if conversation_history:
            messages.extend(conversation_history)
        messages.append({"role": "user", "content": english_text})

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=200,
            temperature=0.7,
        )
        return completion.choices[0].message.content.strip()

    except Exception as exc:
        logger.error("LLM call failed: %s", exc)
        reply = FALLBACK_REPLIES[_fallback_index % len(FALLBACK_REPLIES)]
        _fallback_index += 1
        return reply
