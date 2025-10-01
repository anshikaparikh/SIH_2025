import random
import cv2
import numpy as np
from typing import Tuple

class ForgeryDetectionService:
    def __init__(self):
        pass
    
    def detect_forgery(self, image_path: str) -> float:
        """
        Detect forgery in certificate image
        Returns forgery probability between 0.0 (authentic) and 1.0 (forged)
        """
        # Check if it's a PDF
        if image_path.lower().endswith('.pdf'):
            # For demo purposes, return a random forgery score for PDFs
            return random.uniform(0.1, 0.4)  # Low to medium forgery probability

        # Load image
        img = cv2.imread(image_path)
        if img is None:
            return 1.0  # High forgery if can't load

        # Simple mock detection: analyze edges, noise, etc.
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Edge detection
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])

        # Noise level
        noise = np.std(gray)

        # Mock score based on features
        forgery_score = 0.0
        if edge_density < 0.05:  # Too smooth, suspicious
            forgery_score += 0.3
        if noise > 50:  # Too noisy, possible tampering
            forgery_score += 0.4
        forgery_score += random.uniform(0, 0.3)  # Random component

        return min(forgery_score, 1.0)
