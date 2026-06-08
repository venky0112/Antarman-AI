"""LLM Agent — generates empathetic mental-health responses using Google Gemini only.

Only using Google Gemini 2.5-Flash with system instruction.
Set GEMINI_API_KEY in backend/.env to enable responses.
"""

import os
import logging
import time

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

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
    """Generate an empathetic response to *english_text* using Google Gemini only.

    Args:
        english_text:         The user's message already translated to English.
        conversation_history: Optional list of prior messages in format
                              [{"role": "user"|"assistant", "content": "..."}]

    Returns:
        An English response string.
        
    Raises:
        RuntimeError: If GEMINI_API_KEY is not set or Gemini API call fails.
    """
    
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY not set. Please add it to backend/.env file. "
            "Get your key from: https://ai.google.dev/metrics/explorer"
        )
    
    try:
        import google.generativeai as genai
        
        logger.info("Initializing Google Gemini 1.5-Flash...")
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Create model with system instruction
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            system_instruction=SYSTEM_PROMPT,
        )
        
        logger.info("Building conversation context...")
        # Build message history for multi-turn context
        messages = []
        if conversation_history:
            # Use last 6 turns (3 user + 3 assistant) for context
            for msg in conversation_history[-6:]:
                role = "user" if msg["role"] == "user" else "model"
                messages.append({"role": role, "parts": msg["content"]})
        
        # Add current user message
        messages.append({"role": "user", "parts": english_text})
        
        logger.info(f"Sending request to Gemini (text length: {len(english_text)} chars)...")
        
        # Call Gemini API with retries
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = model.generate_content(
                    messages,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.8,
                        max_output_tokens=300,
                        top_p=0.95,
                    )
                )
                
                # Extract text from response
                if response and response.text:
                    result_text = response.text.strip()
                    logger.info(f"✓ Gemini response received ({len(result_text)} chars)")

                    # Heuristic: if response looks truncated (very short or no ending punctuation),
                    # request a short continuation to complete the thought. This keeps extra calls
                    # minimal and only triggers when needed.
                    if len(result_text) < 40 or result_text[-1] not in '.!?':
                        try:
                            logger.info("Response looks truncated; requesting brief continuation...")
                            cont_prompt = (
                                "Please continue the previous assistant reply briefly (1-2 sentences), "
                                "keeping the same empathetic tone."
                            )
                            cont_messages = [
                                {"role": "user", "parts": english_text},
                                {"role": "assistant", "parts": result_text},
                                {"role": "user", "parts": cont_prompt},
                            ]
                            cont_resp = model.generate_content(
                                cont_messages,
                                generation_config=genai.types.GenerationConfig(
                                    temperature=0.7,
                                    max_output_tokens=120,
                                    top_p=0.9,
                                )
                            )
                            if cont_resp and cont_resp.text:
                                more = cont_resp.text.strip()
                                # Append the continuation to original (avoid duplication)
                                if more and more not in result_text:
                                    result_text = (result_text + " " + more).strip()
                        except Exception as cont_err:
                            logger.warning("Continuation attempt failed: %s", cont_err)

                    return result_text
                else:
                    logger.warning("Gemini returned empty response, retrying...")
                    if attempt < max_retries - 1:
                        time.sleep(1)
                        continue
                    return "I'm having trouble responding right now. Please try again."
                    
            except Exception as api_error:
                logger.error(f"Attempt {attempt + 1}/{max_retries} failed: {api_error}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise
        
    except ImportError as exc:
        logger.error(f"google-generativeai library not installed: {exc}")
        raise RuntimeError(
            "google-generativeai not installed. Install with: pip install google-generativeai"
        ) from exc
        
    except Exception as exc:
        logger.error(f"Gemini API call failed: {exc}", exc_info=True)
        raise RuntimeError(f"Failed to get Gemini response: {exc}") from exc
