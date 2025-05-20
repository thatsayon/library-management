from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (
    UserRegistrationAPIView,
    BookInfoAPIView,
    AuthorsAPIView,
    CategoryAPIView,
    BorrowBookAPIView,
    BookReturnAPIView,
    GetPenaltiesInfoAPIView,
)

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view()),
    path('login/', TokenObtainPairView.as_view()),

    path('book/', BookInfoAPIView.as_view()),
    path('book/<uuid:id>/', BookInfoAPIView.as_view()),

    path('authors/', AuthorsAPIView.as_view()),
    path('categories/', CategoryAPIView.as_view()),

    path('borrow/', BorrowBookAPIView.as_view()),
    path('return/', BookReturnAPIView.as_view()),

    path('users/<uuid:id>/penalties/', GetPenaltiesInfoAPIView.as_view()),
]