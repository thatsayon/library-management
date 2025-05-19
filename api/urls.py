from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import UserRegistrationAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
]