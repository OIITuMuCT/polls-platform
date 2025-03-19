from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Book, UserBookRelation

# Register your models here.
# admin.site.register(Book)

@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_filter = ['title', 'price']
    list_display= ['title', 'price', 'author']

@admin.register(UserBookRelation)
class UserBookRelationAdmin(ModelAdmin):
    pass