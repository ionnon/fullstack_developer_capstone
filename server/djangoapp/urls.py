from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from . import capstone_fix_views as capfix

app_name = "djangoapp"

urlpatterns = [
    # CAPSTONE_PRIORITY_ROUTES
    path('fetchDealers', capfix.fetch_dealers, name='fetchDealers'),
    path('fetchDealers/<str:state>', capfix.fetch_dealers_by_state, name='fetchDealersByState'),
    path('get_dealers', capfix.fetch_dealers, name='get_dealers_fixed'),
    path('get_dealers/<str:state>', capfix.fetch_dealers_by_state, name='get_dealers_state_fixed'),
    path('dealer/<int:dealer_id>', capfix.dealer_by_id, name='dealer_by_id_fixed'),
    path('get_cars', capfix.get_cars, name='get_cars_fixed'),
    path('get_car_makes', capfix.get_car_makes, name='get_car_makes_fixed'),
    path('reviews/dealer/<int:dealer_id>', capfix.get_dealer_reviews, name='dealer_reviews_fixed'),
    path('add_review', capfix.add_review, name='add_review_fixed'),
    path('logout', capfix.logout_fixed, name='logout_fixed'),

    path('fetchDealers', capfix.fetch_dealers, name='fetchDealers'),
    path('fetchDealers/<str:state>', capfix.fetch_dealers_by_state, name='fetchDealersByState'),
    path('get_dealers', capfix.fetch_dealers, name='get_dealers_fixed'),
    path('get_dealers/<str:state>', capfix.fetch_dealers_by_state, name='get_dealers_state_fixed'),
    path('dealer/<int:dealer_id>', capfix.dealer_by_id, name='dealer_by_id_fixed'),
    path('get_cars', capfix.get_cars, name='get_cars_fixed'),
    path('logout', capfix.logout_fixed, name='logout_fixed'),

    path("login", views.login_user, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("register", views.registration, name="register"),
    path("get_dealers", views.get_dealerships, name="get_dealers"),
    path("get_dealers/<str:state>", views.get_dealerships, name="get_dealers_by_state"),
    path("reviews/dealer/<int:dealer_id>", views.get_dealer_reviews, name="dealer_reviews"),
    path("dealer/<int:dealer_id>", views.get_dealer_details, name="dealer_details"),
    path("add_review", views.add_review, name="add_review"),
    path("get_cars", views.get_cars, name="get_cars"),
    path("get_car_makes", views.get_car_makes, name="get_car_makes"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
