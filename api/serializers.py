from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Book, Author, Category, Borrow

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, data):
        user = User.objects.create_regularuser(
            email=data['email'],
            username=data['username'],
            password=data['password']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class BookInfoSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'author', 'category']
        read_only_fields = ['id']

    def get_author(self, book):
        return book.author.name
    
    def get_category(self, book):
        return book.category.name

class BookCreateSerializer(serializers.ModelSerializer):
    author = serializers.UUIDField()
    category = serializers.UUIDField()

    class Meta:
        model = Book
        fields = ['title', 'description', 'author', 'category', 'total_copies']

    def create(self, data):
        author_id = data.pop('author')
        category_id = data.pop('category')

        author_info = Author.objects.get(id=author_id)
        category_info = Category.objects.get(id=category_id)

        book = Book.objects.create(author=author_info, category=category_info, **data)
        return book

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio']
        read_only_fields = ['id']

    def create(self, data):
        author = Author.objects.create(
            name=data['name'],
            bio=data['bio']
        )
        author.save()
        return author

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']

    def create(self, data):
        category = Category.objects.create(name=data['name'])
        category.save()
        return category
    
class BorrowListSerializser(serializers.ModelSerializer):
    book = serializers.CharField(source='book.title')
    class Meta:
        model = Borrow
        fields = ['id', 'book', 'borrow_date', 'due_date']
        read_only_fields = ['id']

class PenaltyPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'penalty_point']