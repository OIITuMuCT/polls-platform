from django.db import models


class Book(models.Model):
    """
    Класс книга 
    attr: title, price """
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    author = models.CharField(max_length=255)

    def __str__(self):
        return self.title