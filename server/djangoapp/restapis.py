import os
import requests
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

backend_url = os.getenv("backend_url", default="http://localhost:3030")
sentiment_analyzer_url = os.getenv("sentiment_analyzer_url", default="http://localhost:5050/")


def get_request(endpoint, **kwargs):
    request_url = backend_url + endpoint
    response = requests.get(request_url, params=kwargs, timeout=15)
    response.raise_for_status()
    return response.json()


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url.rstrip("/") + "/analyze/" + quote(text)
    response = requests.get(request_url, timeout=15)
    response.raise_for_status()
    return response.json()


def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    response = requests.post(request_url, json=data_dict, timeout=15)
    response.raise_for_status()
    return response.json()
