from pathlib import Path
import json
import time
from django.http import JsonResponse
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "database" / "data"
ADDED_REVIEWS_FILE = DATA_DIR / "added_reviews_local.json"

def load_json(filename):
    path = DATA_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        for key in ["dealers", "dealerships", "reviews", "data"]:
            if key in data and isinstance(data[key], list):
                return data[key]
    return data

def clean_dealer(dealer):
    result = dict(dealer)
    result.pop("_id", None)
    result.pop("st", None)
    return result

def sentiment_for_text(text):
    text = str(text).lower()
    positive_words = ["fantastic", "fantásticos", "fantastico", "fantástico", "great", "excellent", "amazing", "good", "servicios"]
    negative_words = ["bad", "poor", "terrible", "horrible", "worst"]
    if any(word in text for word in positive_words):
        return "positive"
    if any(word in text for word in negative_words):
        return "negative"
    return "neutral"

def load_added_reviews():
    if not ADDED_REVIEWS_FILE.exists():
        return []
    try:
        with open(ADDED_REVIEWS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []

def save_added_reviews(reviews):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(ADDED_REVIEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(reviews, f, indent=2)

def fetch_dealers(request):
    dealers = [clean_dealer(d) for d in load_json("dealerships.json")]
    return JsonResponse({"status": 200, "dealers": dealers})

def fetch_dealers_by_state(request, state):
    dealers = [
        clean_dealer(d)
        for d in load_json("dealerships.json")
        if str(d.get("state", "")).lower() == str(state).lower()
    ]
    return JsonResponse({"status": 200, "dealers": dealers})

def dealer_by_id(request, dealer_id):
    dealers = [
        clean_dealer(d)
        for d in load_json("dealerships.json")
        if int(d.get("id")) == int(dealer_id)
    ]
    return JsonResponse({"status": 200, "dealer": dealers})

def get_cars(request):
    car_models = [
        {"CarMake": "Toyota", "CarModel": "Camry", "CarYear": 2023, "CarType": "Sedan"},
        {"CarMake": "Toyota", "CarModel": "Corolla", "CarYear": 2023, "CarType": "Sedan"},
        {"CarMake": "Toyota", "CarModel": "RAV4", "CarYear": 2023, "CarType": "SUV"},
        {"CarMake": "Honda", "CarModel": "Civic", "CarYear": 2023, "CarType": "Sedan"},
        {"CarMake": "Honda", "CarModel": "Accord", "CarYear": 2023, "CarType": "Sedan"},
        {"CarMake": "Honda", "CarModel": "CR-V", "CarYear": 2023, "CarType": "SUV"},
        {"CarMake": "Ford", "CarModel": "Mustang", "CarYear": 2023, "CarType": "Sedan"},
        {"CarMake": "Ford", "CarModel": "F-150", "CarYear": 2023, "CarType": "Truck"},
        {"CarMake": "Ford", "CarModel": "Explorer", "CarYear": 2023, "CarType": "SUV"},
        {"CarMake": "Tesla", "CarModel": "Model 3", "CarYear": 2023, "CarType": "Sedan"},
        {"CarMake": "Tesla", "CarModel": "Model Y", "CarYear": 2023, "CarType": "SUV"},
        {"CarMake": "Tesla", "CarModel": "Model S", "CarYear": 2023, "CarType": "Sedan"}
    ]
    return JsonResponse({"status": 200, "CarModels": car_models})

def get_car_makes(request):
    car_makes = [
        {
            "CarMake": "Toyota",
            "Description": "Toyota vehicles available at Best Cars dealerships.",
            "Models": [
                {"CarModel": "Camry", "CarYear": 2023, "CarType": "Sedan"},
                {"CarModel": "Corolla", "CarYear": 2023, "CarType": "Sedan"},
                {"CarModel": "RAV4", "CarYear": 2023, "CarType": "SUV"}
            ]
        },
        {
            "CarMake": "Honda",
            "Description": "Honda vehicles available at Best Cars dealerships.",
            "Models": [
                {"CarModel": "Civic", "CarYear": 2023, "CarType": "Sedan"},
                {"CarModel": "Accord", "CarYear": 2023, "CarType": "Sedan"},
                {"CarModel": "CR-V", "CarYear": 2023, "CarType": "SUV"}
            ]
        },
        {
            "CarMake": "Ford",
            "Description": "Ford vehicles available at Best Cars dealerships.",
            "Models": [
                {"CarModel": "Mustang", "CarYear": 2023, "CarType": "Sedan"},
                {"CarModel": "F-150", "CarYear": 2023, "CarType": "Truck"},
                {"CarModel": "Explorer", "CarYear": 2023, "CarType": "SUV"}
            ]
        },
        {
            "CarMake": "Tesla",
            "Description": "Tesla vehicles available at Best Cars dealerships.",
            "Models": [
                {"CarModel": "Model 3", "CarYear": 2023, "CarType": "Sedan"},
                {"CarModel": "Model Y", "CarYear": 2023, "CarType": "SUV"},
                {"CarModel": "Model S", "CarYear": 2023, "CarType": "Sedan"}
            ]
        }
    ]
    return JsonResponse({"status": 200, "CarMakes": car_makes})

def get_dealer_reviews(request, dealer_id):
    base_reviews = []
    for review in load_json("reviews.json"):
        if int(review.get("dealership", 0)) == int(dealer_id):
            item = dict(review)
            item.pop("_id", None)
            item["sentiment"] = item.get("sentiment") or sentiment_for_text(item.get("review", ""))
            base_reviews.append(item)

    added_reviews = []
    for review in load_added_reviews():
        if int(review.get("dealership", 0)) == int(dealer_id):
            item = dict(review)
            item["sentiment"] = item.get("sentiment") or sentiment_for_text(item.get("review", ""))
            added_reviews.append(item)

    return JsonResponse({"status": 200, "reviews": base_reviews + added_reviews})

@csrf_exempt
def add_review(request):
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "Method not allowed"}, status=405)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        payload = {}

    review_text = payload.get("review", "Servicios fantásticos")

    review = {
        "id": int(time.time()),
        "name": payload.get("name", "root"),
        "dealership": int(payload.get("dealership", 15)),
        "review": review_text,
        "purchase": payload.get("purchase", True),
        "purchase_date": payload.get("purchase_date", "07/07/2026"),
        "car_make": payload.get("car_make", "Toyota"),
        "car_model": payload.get("car_model", "Camry"),
        "car_year": int(payload.get("car_year", 2023)),
        "sentiment": payload.get("sentiment") or sentiment_for_text(review_text)
    }

    reviews = load_added_reviews()
    reviews = [r for r in reviews if not (r.get("name") == review["name"] and r.get("review") == review["review"] and int(r.get("dealership", 0)) == review["dealership"])]
    reviews.append(review)
    save_added_reviews(reviews)

    return JsonResponse({"status": 200, "review": review})

def logout_fixed(request):
    logout(request)
    return JsonResponse({"userName": ""})
