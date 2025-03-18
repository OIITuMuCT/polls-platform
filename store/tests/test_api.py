from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Book
from store.serializers import BookSerializer
class BooksApiTest(APITestCase):

    def test_get(self):
        """тест: получение api объекта Book"""
        book_1 = Book.objects.create(title='Test Book 1', price=25)
        book_2 = Book.objects.create(title="Test Book 2", price=55)
        url = reverse('book-list')
        print(url)
        response = self.client.get(url)
        serializer_data = BookSerializer([book_1, book_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

        print(response.data)
