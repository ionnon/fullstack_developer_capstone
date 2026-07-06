from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json

from .models import CarMake, CarModel
from .restapis import get_request, post_review, analyze_review_sentiments


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"status": "Invalid request"}, status=405)

    data = json.loads(request.body)
    username = data.get("userName")
    password = data.get("password")

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({
            "userName": username,
            "firstName": user.first_name,
            "lastName": user.last_name,
            "status": "Authenticated"
        })

    return JsonResponse({"userName": username, "status": "Failed"})


def logout_request(request):
    logout(request)
    return JsonResponse({"status": "Logged out"})


@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse({"status": "Invalid request"}, status=405)

    data = json.loads(request.body)
    username = data.get("userName")
    password = data.get("password")
    first_name = data.get("firstName", "")
    last_name = data.get("lastName", "")
    email = data.get("email", "")

    if User.objects.filter(username=username).exists():
        return JsonResponse({"userName": username, "status": "User already exists"}, status=400)

    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email
    )

    login(request, user)

    return JsonResponse({
        "userName": username,
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "status": "Registered"
    })


def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"

    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    reviews = get_request(f"/fetchReviews/dealer/{dealer_id}")

    for review in reviews:
        review_text = review.get("review", "")
        try:
            sentiment = analyze_review_sentiments(review_text)
            review["sentiment"] = sentiment.get("sentiment", "neutral")
        except Exception:
            review["sentiment"] = "neutral"

    return JsonResponse({"status": 200, "reviews": reviews})


def get_dealer_details(request, dealer_id):
    dealer = get_request(f"/fetchDealer/{dealer_id}")
    return JsonResponse({"status": 200, "dealer": dealer})


@csrf_exempt
def add_review(request):
    if request.method != "POST":
        return JsonResponse({"status": "Invalid request"}, status=405)

    data = json.loads(request.body)

    try:
        sentiment = analyze_review_sentiments(data.get("review", ""))
        data["sentiment"] = sentiment.get("sentiment", "neutral")
    except Exception:
        data["sentiment"] = "neutral"

    response = post_review(data)
    return JsonResponse({"status": 200, "review": response})


def get_cars(request):
    car_models = CarModel.objects.select_related("make").all()
    cars = [
        {
            "CarMake": car.make.name,
            "CarModel": car.name,
            "CarYear": car.year,
            "CarType": car.type
        }
        for car in car_models
    ]
    return JsonResponse({"status": 200, "CarModels": cars})


def get_car_makes(request):
    makes = CarMake.objects.all()
    data = []
    for make in makes:
        models = CarModel.objects.filter(make=make)
        data.append({
            "CarMake": make.name,
            "Description": make.description,
            "Models": [
                {
                    "CarModel": model.name,
                    "CarYear": model.year,
                    "CarType": model.type
                }
                for model in models
            ]
        })
    return JsonResponse({"status": 200, "CarMakes": data})
