"""Translation module using deep-translator (Google Translate) as the primary engine.

Supports English ↔ all major Indian languages (Hindi, Tamil, Telugu, Bengali,
Marathi, Gujarati, Kannada, Malayalam, Punjabi, Odia, Urdu, etc.).
No API key required. Falls back to a static phrase dictionary if offline.
"""

import logging

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Static offline fallback dictionary (used only when network is unavailable)
# ---------------------------------------------------------------------------
FALLBACK_TO_EN: dict[str, dict[str, str]] = {
    "hi": {
        "नमस्ते": "hello",
        "आप कैसे हैं": "how are you",
        "मुझे चिंता हो रही है": "i am feeling anxious",
        "मुझे दुख हो रहा है": "i am feeling sad",
        "मुझे अच्छा नहीं लग रहा": "i am not feeling well",
    },
    "ta": {
        "வணக்கம்": "hello",
        "நீங்கள் எப்படி இருக்கிறீர்கள்": "how are you",
        "எனக்கு பதட்டமாக இருக்கிறது": "i am feeling anxious",
        "எனக்கு வருத்தமாக இருக்கிறது": "i am feeling sad",
    },
    "te": {
        "నమస్కారం": "hello",
        "మీరు ఎలా ఉన్నారు": "how are you",
    },
    "bn": {
        "হ্যালো": "hello",
        "আপনি কেমন আছেন": "how are you",
    },
}

FALLBACK_FROM_EN: dict[str, dict[str, str]] = {
    lang: {v: k for k, v in phrases.items()}
    for lang, phrases in FALLBACK_TO_EN.items()
}


# ---------------------------------------------------------------------------
# Core translation helpers
# ---------------------------------------------------------------------------

def _google_translate(text: str, source: str, target: str) -> str:
    """Call Google Translate via deep-translator. Returns '' on any failure."""
    try:
        from deep_translator import GoogleTranslator
        result = GoogleTranslator(source=source, target=target).translate(text)
        return result or ""
    except Exception as exc:
        logger.warning("GoogleTranslator failed (%s → %s): %s", source, target, exc)
        return ""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def translate_to_english(text: str, src_lang: str) -> str:
    """Translate *text* from *src_lang* to English.

    Args:
        text:     Input text in the source language.
        src_lang: BCP-47 / ISO 639-1 language code (e.g. 'hi', 'ta', 'en').

    Returns:
        Translated English string.
    """
    if src_lang == "en":
        return text

    # Primary: Google Translate
    result = _google_translate(text, source=src_lang, target="en")
    if result:
        return result

    # Offline fallback: static dictionary
    phrases = FALLBACK_TO_EN.get(src_lang, {})
    for native, eng in phrases.items():
        if text.strip().lower() == native.lower():
            return eng

    logger.warning("All translation methods failed for '%s' (%s→en)", text, src_lang)
    return text


def translate_from_english(text: str, tgt_lang: str) -> str:
    """Translate *text* from English to *tgt_lang*.

    Args:
        text:     Input text in English.
        tgt_lang: BCP-47 / ISO 639-1 language code (e.g. 'hi', 'ta').

    Returns:
        Translated string in the target language.
    """
    if tgt_lang == "en":
        return text

    # Primary: Google Translate
    result = _google_translate(text, source="en", target=tgt_lang)
    if result:
        return result

    # Offline fallback: static dictionary
    phrases = FALLBACK_FROM_EN.get(tgt_lang, {})
    for eng, native in phrases.items():
        if text.strip().lower() == eng.lower():
            return native

    logger.warning("All translation methods failed for '%s' (en→%s)", text, tgt_lang)
    return "{} [Translated to {}]".format(text, tgt_lang)