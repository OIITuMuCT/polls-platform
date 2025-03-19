import json
from django.urls import reverse
from unittest import skip
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Book
from store.serializers import BookSerializer
from django.contrib.auth.models import User


class BooksApiTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_username")
        self.book_1 = Book.objects.create(title='Test Book 1', price=25, author='Author 1')
        self.book_2 = Book.objects.create(title="Test Book 2", price=55, author='Author 2')
        self.book_3 = Book.objects.create(title="Test Book 3 Author 1", price=55, author='Author 1')

    def test_get(self):
        """тест: получение api объекта Book"""

        url = reverse('book-list')
        print(url)
        response = self.client.get(url)
        serializer_data = BookSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        print(response.data)

    @skip
    def test_get_filter(self):
        """тест: получение filter"""
        url = reverse("book-list")
        print(url)
        response = self.client.get(url, data={'price': 55})
        serializer_data = BookSerializer([self.book_1, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        print(response.data)

    def test_get_search(self):
        """тест: получение search"""
        url = reverse("book-list")
        print(url)
        response = self.client.get(url, data={"search": "Author 1"})
        serializer_data = BookSerializer([self.book_1, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        print(response.data)

    def test_create(self):
        """тест: создание объекта Book"""
        url = reverse("book-list")
        data = {
            "title": "For Whom The Bell Tolls",
            "price": 1000,
            "author": "Ernest Hemingway",
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        print(url)
        response = self.client.post(url, data=json_data, content_type="application/json")

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        print(response.data)
