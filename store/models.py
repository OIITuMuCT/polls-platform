from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    """
    Класс книга 
    attr: title, price, author """
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    author = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.title

class UserBookRelation(models.Model):
    pass