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
            import os
            hf_token = os.getenv("HF_TOKEN", "")
            
            # Use the specified model ID or default to the private one
            model_id = os.getenv("CRISIS_MODEL_ID", "cogint/suicidality-detection")
            
            try:
                logger.info(f"Attempting to load crisis model: {model_id}")
                self.pipeline = pipeline(
                    "text-classification",
                    model=model_id,
                    tokenizer=model_id,
                    token=hf_token if hf_token else None,
                    return_all_scores=True,
                    truncation=True,
                    max_length=512,
                )
            except Exception as primary_err:
                # If it's a 404 (private/missing), fallback to a public alternative
                public_fallback = "sentinet/suicidality"
                logger.warning(
                    f"Could not load primary model '{model_id}' (Error: {primary_err}). "
                    f"Falling back to public model: {public_fallback}"
                )
                self.pipeline = pipeline(
                    "text-classification",
                    model=public_fallback,
                    tokenizer=public_fallback,
                    return_all_scores=True,
                    truncation=True,
                    max_length=512,
                )
            
            logger.info("Crisis model loaded successfully.")
        except Exception as e:
            logger.warning("Could not load any HuggingFace model, using fallback regex. Error: %s", e)

    def predict(self, text: str) -> bool:
        if self.pipeline is not None:
            try:
                raw = self.pipeline(text)
                
                # Normalize raw results into a flat list of dicts
                flat_results = []
                if isinstance(raw, list):
                    if len(raw) > 0 and isinstance(raw[0], list):
                        flat_results = raw[0]  # Nested list: [[{...}]] -> [{...}]
                    else:
                        flat_results = raw  # Flat list: [{...}]
                elif isinstance(raw, dict):
                    flat_results = [raw]  # Dict: {...} -> [{...}]
                
                suicide_score = 0.0
                for res in flat_results:
                    if isinstance(res, dict) and "label" in res and "score" in res:
                        label = str(res["label"]).lower()
                        # Match 'suicide', 'suicidal', or 'label_1' (often positive class in models)
                        if "suicide" in label or "suicidal" in label or label == "label_1":
                            suicide_score = max(suicide_score, res["score"])
                
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
