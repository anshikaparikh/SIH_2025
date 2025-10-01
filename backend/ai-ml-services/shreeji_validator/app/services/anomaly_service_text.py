import pandas as pd
from fuzzywuzzy import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.utils.text_cleaning import clean_text

class TextAnomalyService:
    def __init__(self, labels_path='data/labels.csv'):
        """
        labels_path: CSV containing 'name', 'course', 'date' columns
        """
        self.labels_df = pd.read_csv(labels_path)
        self.labels_df = self.labels_df.fillna('')
        # Clean label data upfront
        self.labels_df['combined'] = (
            self.labels_df['name'].astype(str) + " " +
            self.labels_df['course'].astype(str) + " " +
            self.labels_df['date'].astype(str)
        ).apply(clean_text)

    def fuzzy_match(self, extracted_text, threshold=80):
        """
        Returns best match using fuzzy ratio
        """
        best_score = 0
        best_index = None
        for idx, label_text in enumerate(self.labels_df['combined']):
            score = fuzz.token_sort_ratio(extracted_text, label_text)
            if score > best_score:
                best_score = score
                best_index = idx

        if best_score >= threshold:
            status = 'HIGH MATCH'
        elif best_score >= threshold - 20:
            status = 'MEDIUM MATCH'
        else:
            status = 'LOW MATCH'

        return {
            'status': status,
            'score': best_score,
            'matched_label': self.labels_df.iloc[best_index].to_dict() if best_index is not None else None
        }

    def tfidf_cosine_match(self, extracted_text):
        """
        Returns cosine similarity with all labels
        """
        corpus = list(self.labels_df['combined']) + [clean_text(extracted_text)]
        vectorizer = TfidfVectorizer().fit_transform(corpus)
        cosine_matrix = cosine_similarity(vectorizer[-1], vectorizer[:-1])
        best_idx = cosine_matrix.argmax()
        best_score = cosine_matrix[0, best_idx]

        if best_score > 0.8:
            status = 'HIGH MATCH'
        elif best_score > 0.6:
            status = 'MEDIUM MATCH'
        else:
            status = 'LOW MATCH'

        return {
            'status': status,
            'score': round(float(best_score*100), 2),
            'matched_label': self.labels_df.iloc[best_idx].to_dict()
        }

# Example usage
if __name__ == "__main__":
    extracted_text = """
    Anshika Parikh completed Python Bootcamp on 24-09-2025
    """
    anomaly_service = TextAnomalyService(labels_path='data/labels.csv')
    
    fuzzy_result = anomaly_service.fuzzy_match(clean_text(extracted_text))
    cosine_result = anomaly_service.tfidf_cosine_match(extracted_text)

    print("=== Fuzzy Match Result ===")
    print(fuzzy_result)

    print("\n=== TF-IDF Cosine Match Result ===")
    print(cosine_result)
