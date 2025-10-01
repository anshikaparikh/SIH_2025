import random
import re
from typing import List

class TextAnomalyService:
    def __init__(self):
        self.common_patterns = [
            r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # Names
            r'\b\d{4}\b',  # Years
            r'\b[A-Z]{2,5}\b',  # Acronyms
        ]
    
    def detect_anomalies(self, text: str) -> float:
        """
        Detect text anomalies (e.g., unusual patterns, inconsistencies)
        Returns anomaly score between 0.0 (normal) and 1.0 (highly anomalous)
        """
        # Simple mock: count unusual characters or patterns
        anomalies = 0
        total_chars = len(text)
        
        # Check for excessive numbers or symbols
        if len(re.findall(r'\d', text)) / total_chars > 0.3:
            anomalies += 1
        
        # Check for repeated words (potential OCR error)
        words = text.split()
        word_counts = {}
        for word in words:
            word_counts[word.lower()] = word_counts.get(word.lower(), 0) + 1
        
        repeated = sum(1 for count in word_counts.values() if count > 2)
        if repeated > 3:
            anomalies += 1
        
        # Mock randomness for demo
        anomalies += random.uniform(0, 1)
        
        score = min(anomalies / 3.0, 1.0)  # Normalize
        return score
