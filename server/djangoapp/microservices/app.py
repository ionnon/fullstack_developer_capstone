from flask import Flask
from nltk.sentiment import SentimentIntensityAnalyzer
import json
import unicodedata

app = Flask("Sentiment Analyzer")
sia = SentimentIntensityAnalyzer()


def normalize_text(text):
    text = text.lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join([c for c in text if not unicodedata.combining(c)])
    return text


@app.get("/")
def home():
    return "Welcome to the Sentiment Analyzer. Use /analyze/text to get the sentiment"


@app.get("/analyze/<input_txt>")
def analyze_sentiment(input_txt):
    normalized = normalize_text(input_txt)

    positive_words = [
        "fantastico", "fantasticos", "fantastica", "fantasticas",
        "excelente", "excelentes", "bueno", "buenos", "buena", "buenas",
        "great", "excellent", "fantastic", "amazing", "good", "love"
    ]

    negative_words = [
        "malo", "malos", "mala", "malas", "terrible", "horrible",
        "bad", "poor", "awful", "worst", "hate"
    ]

    if any(word in normalized for word in positive_words):
        return json.dumps({"sentiment": "positive"})

    if any(word in normalized for word in negative_words):
        return json.dumps({"sentiment": "negative"})

    scores = sia.polarity_scores(input_txt)
    pos = float(scores["pos"])
    neg = float(scores["neg"])
    neu = float(scores["neu"])

    res = "positive"
    if neg > pos and neg > neu:
        res = "negative"
    elif neu > neg and neu > pos:
        res = "neutral"

    return json.dumps({"sentiment": res})


if __name__ == "__main__":
    app.run(debug=True)
