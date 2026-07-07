"""djangoproj URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),

    path('', TemplateView.as_view(template_name="Home.html"), name='home'),
    path('about/', TemplateView.as_view(template_name="About.html"), name='about'),
    path('contact/', TemplateView.as_view(template_name="Contact.html"), name='contact'),

    path('dealers/', TemplateView.as_view(template_name="Home.html"), name='dealers'),
    path("dealers/<str:state>/", TemplateView.as_view(template_name="Home.html"), name="dealers_by_state_page"),
    path('dealer/<int:id>/', TemplateView.as_view(template_name="Home.html"), name='dealer_detail'),
    path('postreview/<int:id>/', TemplateView.as_view(template_name="Home.html"), name='post_review'),
    path('login/', TemplateView.as_view(template_name="Home.html"), name='login'),
    path('register/', TemplateView.as_view(template_name="Home.html"), name='register'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
