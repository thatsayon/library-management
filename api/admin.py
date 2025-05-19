from django.contrib import admin
from .models import (
    UserAccount,
    Author,
    Category,
    Book,
)

admin.site.register(UserAccount)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Book)