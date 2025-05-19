from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (
    UserRegistrationAPIView,
    BookInfoAPIView,
    AuthorsAPIView,
    CategoryAPIView,
)

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view()),
    path('login/', TokenObtainPairView.as_view()),

    path('book/', BookInfoAPIView.as_view()),
    path('book/<uuid:id>/', BookInfoAPIView.as_view()),

    path('authors/', AuthorsAPIView.as_view()),
    path('categories/', CategoryAPIView.as_view()),
]