from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# -----------------------------
# Flask App Setup
# -----------------------------
app = Flask(__name__)
CORS(app)

# -----------------------------
# NLTK Safe Download (Render-safe)
# -----------------------------
try:
    nltk.data.find("corpora/stopwords")
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("stopwords")
    nltk.download("wordnet")

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

# -----------------------------
# Load ML Artifacts
# -----------------------------
model = joblib.load("model/spam_classifier_model.pkl")
tfidf = joblib.load("model/tfidf_vectorizer.pkl")

# -----------------------------
# Text Preprocessing
# -----------------------------
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    words = text.split()
    words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words]
    return " ".join(words)

# -----------------------------
# Health Check Route
# -----------------------------
@app.route("/", methods=["GET"])
def health():
    return "Backend is running"

# -----------------------------
# Prediction Route
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        subject = data.get("subject", "")
        body = data.get("body", "")

        combined_text = preprocess_text(subject + " " + body)

        # Handle empty or meaningless input safely
        if not combined_text.strip():
            return jsonify({"prediction": "Not Spam"}), 200

        vector = tfidf.transform([combined_text])
        prediction = model.predict(vector)[0]

        return jsonify({
            "prediction": "Spam" if prediction == 1 else "Not Spam"
        })

    except Exception as e:
        print("PREDICTION ERROR:", str(e))
        return jsonify({"error": "Prediction failed"}), 500

# -----------------------------
# App Runner (Render-compatible)
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
