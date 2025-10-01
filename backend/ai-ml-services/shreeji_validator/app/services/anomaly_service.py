from app.services.anomaly_service_text import TextAnomalyService
from ml_models.forgery_detection.forgery_service import ForgeryDetector
from app.utils.text_cleaning import clean_text

class AnomalyService:
    def __init__(self, labels_path="data/labels.csv", forgery_model_path=None, text_weight=0.6, image_weight=0.4):
        self.text_svc = TextAnomalyService(labels_path=labels_path)
        self.forgery_detector = ForgeryDetector(model_path=forgery_model_path) if forgery_model_path else ForgeryDetector()
        self.text_weight = text_weight
        self.image_weight = image_weight

    def run_all_checks(self, extracted_text, img_path):
        # Text anomaly
        clean = clean_text(extracted_text)
        fuzzy = self.text_svc.fuzzy_match(clean)
        text_score = fuzzy['score'] / 100.0
        tfidf = self.text_svc.tfidf_cosine_match(clean)
        tfidf_score = float(tfidf['score']) / 100.0
        combined_text_score = max(text_score, tfidf_score)

        # Image forgery detection
        img_res = self.forgery_detector.predict(img_path)
        per_class = img_res.get('per_class', {})
        real_prob = per_class.get('real', None)
        if real_prob is None:
            if img_res['label'].lower() == 'real':
                real_prob = img_res['confidence']
            else:
                real_prob = 1.0 - img_res['confidence']
        image_score = float(real_prob)

        # Fusion
        combined_score = (self.text_weight * combined_text_score) + (self.image_weight * image_score)
        if combined_score >= 0.75:
            verdict = "Genuine"
        elif combined_score >= 0.45:
            verdict = "Suspect"
        else:
            verdict = "Forged"

        return {
            "verdict": verdict,
            "combined_score": round(combined_score, 3),
            "text": {
                "fuzzy": fuzzy,
                "tfidf": tfidf,
                "combined_text_score": round(combined_text_score, 3)
            },
            "image": img_res
        }
