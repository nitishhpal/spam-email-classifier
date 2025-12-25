from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Initialize app
app = Flask(__name__)
CORS(app)

# Load model and vectorizer
model = joblib.load("model/spam_classifier_model.pkl")
tfidf = joblib.load("model/tfidf_vectorizer.pkl")

# NLP setup
nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words]
    return ' '.join(words)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    subject = data.get("subject", "")
    body = data.get("body", "")

    combined = preprocess_text(subject + " " + body)
    vector = tfidf.transform([combined])
    prediction = model.predict(vector)[0]
    probability = model.predict_proba(vector)[0].max()

    return jsonify({
        "prediction": "Spam" if prediction == 1 else "Not Spam",
        "confidence": round(probability * 100, 2)
    })

if __name__ == "__main__":
    app.run(debug=True)
