from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Book, Author, Category
from .serializers import (
    UserRegistrationSerializer, 
    BookInfoSerializer,
    AuthorSerializer,
    CategorySerializer,
    BookCreateSerializer,
)

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