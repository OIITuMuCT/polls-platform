from django.test import TestCase
from django.contrib.auth.models import User
from store.serializers import BookSerializer
from store.models import Book, UserBookRelation


class BooksSerializerTest(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username="user2")
        user3 = User.objects.create(username='user3')

        book_1 = Book.objects.create(title="Test Book 1", price=25, author='Author 1')
        book_2 = Book.objects.create(title="Test Book 2", price=55, author='Author 2')

        UserBookRelation.objects.create(user=user1, book=book_1, like=True)
        UserBookRelation.objects.create(user=user2, book=book_1, like=True)
        UserBookRelation.objects.create(user=user3, book=book_1, like=True)
        
        UserBookRelation.objects.create(user=user1, book=book_2, like=True)
        UserBookRelation.objects.create(user=user2, book=book_2, like=True)
        UserBookRelation.objects.create(user=user3, book=book_2, like=False)

        data = BookSerializer([book_1, book_2], many=True).data
        expected_data = [
            {
                "id": book_1.id, 
                "title": "Test Book 1", 
                "price": '25.00', 
                "author": "Author 1",
                "likes_count": 3,
            },
            {
                "id": book_2.id, 
                "title": "Test Book 2", 
                "price": '55.00', 
                "author": "Author 2",
                "likes_count": 2,
            },
        ]
        self.assertEqual(expected_data, data)
