from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from .models import Book, Author, Category, Borrow
from .serializers import (
    UserRegistrationSerializer, 
    BookInfoSerializer,
    AuthorSerializer,
    CategorySerializer,
    BookCreateSerializer,
    BorrowListSerializser,
    PenaltyPointSerializer,
)

User = get_user_model()

class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "user registration successfull"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookInfoAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id=None):
        if id:
            book = Book.objects.filter(id=id).first()
            if not book:
                return Response({"msg": "no book found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = BookInfoSerializer(book)
            return Response(serializer.data, status=status.HTTP_200_OK)

        author = request.query_params.get("author")
        category = request.query_params.get("category")

        books = Book.objects.all()
        if author:
            books = books.filter(author__name__icontains=author)
        if category:
            books = books.filter(category__name__icontains=category)
        serializer = BookInfoSerializer(books, many=True) 
        return Response(serializer.data)
    
    def post(self, request):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({"msg": "only admin users can add books."}, status=status.HTTP_403_FORBIDDEN)

        serializer = BookCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "book created successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({"msg": "only admin users can delete books"}, status=status.HTTP_401_UNAUTHORIZED)
        book = Book.objects.filter(id=id).first()
        if not book:
            return Response({"msg": "no book found using this id"}, status=status.HTTP_404_NOT_FOUND)
        book.delete()
        return Response({"msg": "book deleted"}, status=status.HTTP_200_OK)
        


class AuthorsAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "new author created"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "new category created"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BorrowBookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        borrow = Borrow.objects.filter(user=request.user)

        serializer = BorrowListSerializser(borrow, many=True)

        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"msg": "no borrow data found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        book_id = request.data.get('book_id')

        if not book_id:
            return Response({"msg": "book_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        book = get_object_or_404(Book, id=book_id)

        current_borrow = Borrow.objects.filter(user=request.user, return_date__isnull=True).count()

        if current_borrow >= 3:
            return Response({"msg": "can't borrow book. borrow limit reached"}, status=status.HTTP_400_BAD_REQUEST)

        if book.available_copies < 1:
            return Response({"msg": "this book is currenlty unavailable"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            book.available_copies -= 1
            book.save()

            borrow = Borrow.objects.create(
                user=request.user,
                book=book,
                borrow_date=date.today(),
                due_date=date.today() + timedelta(days=14)
            )

        return Response({"msg": "borrow info added"}, status=status.HTTP_200_OK)


class BookReturnAPIView(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        borrow_id = request.data.get('borrow_id')
        user = request.user

        if not borrow_id:
            return Response({"msg": "borrow_id required to return a book"}, status=status.HTTP_400_BAD_REQUEST)
        
        borrow = get_object_or_404(Borrow, id=borrow_id)

        if borrow.return_date:
            return Response({"msg": "book already returned"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            today = date.today()
            borrow.return_date = today
            borrow.save()

            date_differ = (today - borrow.due_date).days

            if date_differ > 0:
                user.penalty_point += 1
                user.save()
            
            borrow.book.total_copies += 1
            borrow.book.save()


        return Response({"msg": "book returned successfull"}, status=status.HTTP_200_OK)
    
class GetPenaltiesInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        req_user = request.user
        user = User.objects.get(id=id)

        if not (req_user.is_staff or req_user == user):
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
    
        serializer = PenaltyPointSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)