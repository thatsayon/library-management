from django.contrib import admin
from .models import (
    UserAccount,
    Author,
    Category,
    Book,
    Borrow
)

@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'penalty_point', 'is_active', 'is_staff')

admin.site.register(Author)
admin.site.register(Category)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author')

@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user__username', 'book__title')