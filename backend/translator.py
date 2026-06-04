
"""Translation module using HuggingFace free Inference API (IndicTrans2)."""

import os
import requests
import logging

logger = logging.getLogger(__name__)

HF_TOKEN = os.getenv("HF_TOKEN", "")
# HuggingFace free tier Inference API endpoint
FREE_API_URL = "https://api-inference.huggingface.co/models/ai4bharat/indictrans2-en-indic-distilled-200M"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

FALLBACK_PHRASES = {
    "hi": {
        "hello": "नमस्ते",
        "how are you": "आप कैसे हैं",
        "i am feeling anxious": "मुझे चिंता हो रही है",
        "i am feeling sad": "मुझे दुख हो रहा है"
    },
    "ta": {
        "hello": "வணக்கம்",
        "how are you": "நீங்கள் எப்படி இருக்கிறீர்கள்",
        "i am feeling anxious": "எனக்கு பதட்டமாக இருக்கிறது",
        "i am feeling sad": "எனக்கு வருத்தமாக இருக்கிறது"
    }
}

def _call_free_api(text: str, src_lang: str, tgt_lang: str) -> str:
    if not HF_TOKEN:
        return ""
    payload = {
        "inputs": text,
        "parameters": {"src_lang": src_lang, "tgt_lang": tgt_lang}
    }
    try:
        resp = requests.post(FREE_API_URL, headers=HEADERS, json=payload, timeout=10)
        resp.raise_for_status()
        result = resp.json()
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "")
        return ""
    except Exception as e:
        logger.warning("Free API call failed: %s", e)
        return ""

def _fallback_translate(text: str, src_lang: str, tgt_lang: str) -> str:
    phrases = FALLBACK_PHRASES.get(src_lang, {})
    for eng, native in phrases.items():
        if text.strip().lower() == native:
            return eng
    return "[Translated from {}] {}".format(src_lang, text)

def _fallback_back_translate(text: str, src_lang: str, tgt_lang: str) -> str:
    phrases = FALLBACK_PHRASES.get(tgt_lang, {})
    for eng, native in phrases.items():
        if text.strip().lower() == eng:
            return native
    return "{} [Translated to {}]".format(text, tgt_lang)

def translate_to_english(text: str, src_lang: str) -> str:
    if src_lang == "en":
        return text
    api_result = _call_free_api(text, src_lang, "eng_Latn")
    if api_result:
        return api_result
    return _fallback_translate(text, src_lang, "eng")

def translate_from_english(text: str, tgt_lang: str) -> str:
    if tgt_lang == "en":
        return text
    api_result = _call_free_api(text, "eng_Latn", tgt_lang)
    if api_result:
        return api_result
    return _fallback_back_translate(text, "eng", tgt_lang)