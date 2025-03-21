from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    """
    Класс книга 
    attr: title, price, author, owner, readers, rating """
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    author = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='my_books')
    readers = models.ManyToManyField(User, through="UserBookRelation", related_name='books')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=None, null=True)

    def __str__(self):
        return self.title

class UserBookRelation(models.Model):
    RATE_CHOICES = (
        (1, "Ok"),
        (2, "Fine"),
        (3, "Good"),
        (4, "Amazing"),
        (5, "Incredible"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return f'{self.user.username}: "{self.book.title}", RATE: {self.rate}'
    
    def save(self, *args, **kwargs):
        from store.logic import set_rating
        
        super().save(*args, **kwargs)
        set_rating(self.book)