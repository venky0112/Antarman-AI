"""Crisis detection using DistilBERT and Regex fallback"""

import re
import logging

logger = logging.getLogger(__name__)

# Fallback regex patterns used when transformers is not available
CRISIS_PATTERNS = [
    r"\bsuicide\b",
    r"\bkill\s*myself\b",
    r"\bend\s*my\s*life\b",
    r"\bwant\s*to\s*die\b",
    r"\bno\s*reason\s*to\s*live\b",
    r"\bharm\s*myself\b",
    r"\bself-harm\b",
    r"\bi\s*don'?t\s*want\s*to\s*be\s*alive\b",
    r"\bgoodbye\s*cruel\s*world\b",
]

class ModelCrisisDetector:
    def __init__(self):
        self.pipeline = None
        try:
            from transformers import pipeline
            self.pipeline = pipeline(
                "text-classification",
                model="cogint/suicidality-detection",  # DistilBERT fine-tuned for suicide risk
                tokenizer="cogint/suicidality-detection",
                return_all_scores=True,
                truncation=True,
                max_length=512,
            )
            logger.info("DistilBERT crisis model loaded successfully.")
        except Exception as e:
            logger.warning("Could not load HuggingFace model, using fallback regex. Error: %s", e)

    def predict(self, text: str) -> bool:
        if self.pipeline is not None:
            try:
                results = self.pipeline(text)[0]
                # The model returns scores for labels: 'suicide' vs 'non-suicide'
                suicide_score = 0.0
                for res in results:
                    if res["label"].lower() == "suicide":
                        suicide_score = res["score"]
                        break
                return suicide_score > 0.5
            except Exception as e:
                logger.error("Model inference failed, falling back to regex. Error: %s", e)
        # Fallback regex
        text_lower = text.lower()
        for pattern in CRISIS_PATTERNS:
            if re.search(pattern, text_lower):
                return True
        return False

_detector = ModelCrisisDetector()

def predict_crisis(text: str) -> bool:
    return _detector.predict(text)
