import sys
import os
import logging
import io

if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
logging.basicConfig(level=logging.INFO)

from crisis_detector import predict_crisis
from translator import translate_to_english, translate_from_english

print("Testing Crisis Detector:")
res1 = predict_crisis("I want to end my life")
print("  Crisis statement detection (should be True):", res1)
res2 = predict_crisis("Hello world!")
print("  Normal statement detection (should be False):", res2)

print("\nTesting Translator:")
trans = translate_to_english("नमस्ते, आप कैसे हैं", "hi")
print("  Translation to English:", trans)
back = translate_from_english("Thank you for sharing your feelings.", "hi")
print("  Translation back to Hindi:", back)
