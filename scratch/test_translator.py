try:
    from deep_translator import GoogleTranslator
    print("deep-translator is already installed!")
    translated = GoogleTranslator(source='auto', target='en').translate("नमस्ते")
    print("Translated:", translated)
except ImportError:
    print("deep-translator is not installed.")
