from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# load model
model = joblib.load("model.pkl")

@app.route("/verify", methods=["POST"])
def verify():
    data = request.get_json()
    file_path = data.get("file_path")

    # TODO: OCR + preprocessing
    # For demo, return dummy score
    score = 0.92
    return jsonify({"score": score, "details": "OCR text matched format"})
    
if __name__ == "__main__":
    app.run(port=5000)
