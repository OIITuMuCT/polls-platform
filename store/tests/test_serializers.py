from django.test import TestCase
from django.contrib.auth.models import User
from store.serializers import BookSerializer
from store.models import Book


class BooksSerializerTest(TestCase):
    def test_ok(self):
        book_1 = Book.objects.create(title="Test Book 1", price=25, author='Author 1')
        book_2 = Book.objects.create(title="Test Book 2", price=55, author='Author 2')
        data = BookSerializer([book_1, book_2], many=True).data

        expected_data = [
            {
                "id": book_1.id, 
                "title": "Test Book 1", 
                "price": '25.00', 
                "author": "Author 1",
                "owner": None
            },
            {
                "id": book_2.id, 
                "title": "Test Book 2", 
                "price": '55.00', 
                "author": "Author 2",
                "owner": None
            },
        ]
        self.assertEqual(expected_data, data)
