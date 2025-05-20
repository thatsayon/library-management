from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
import uuid

class CustomUserManager(BaseUserManager):
    def create_regularuser(self, email, username, password, **kwargs):
        if not email:
            return ValueError("Need an email to create account")
        if not username:
            return ValueError("Need a username to create account")
        if not password:
            return ValueError("Need a password to create account")
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, username, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        return self.create_regularuser(email, username, password, **kwargs)

class UserAccount(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=12, unique=True)

    penalty_point = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"Category - {self.name}"

class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=50)
    bio = models.CharField(max_length=128)

    def __str__(self):
        return f"Author - {self.name}"

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=128)
    description = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="books")
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.available_copies is None:
            self.available_copies = self.total_copies
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Book: {self.title} - Available:{self.available_copies}"

class Borrow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='borrow_list')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow_list')
    borrow_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
