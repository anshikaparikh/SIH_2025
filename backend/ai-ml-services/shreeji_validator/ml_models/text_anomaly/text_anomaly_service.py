# ml_models/text_anomaly/text_anomaly_service.py
import os, pickle
from app.utils.text_cleaning import clean_text

MODEL_PATH = "ml_models/text_anomaly/text_anomaly_model.pkl"

class TextAnomalyModel:
    def __init__(self, model_path=MODEL_PATH):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Text anomaly model not found at {model_path}")
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

    def predict_proba(self, raw_text):
        txt = clean_text(raw_text)
        prob = self.model.predict_proba([txt])[0]  # returns [prob_fake, prob_real] or depending on encoding
        # we assume label 1 is real; find index
        # get class mapping:
        if hasattr(self.model, "classes_"):
            classes = list(self.model.classes_)
            if 1 in classes:
                idx = classes.index(1)
                real_prob = float(prob[idx])
            else:
                # fallback: assume second column = real
                real_prob = float(prob[-1])
        else:
            real_prob = float(prob[-1])
        return {"real_probability": real_prob, "raw": txt}
