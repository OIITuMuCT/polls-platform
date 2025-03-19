import json
from django.urls import reverse
from unittest import skip
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase
from store.models import Book, UserBookRelation
from store.serializers import BookSerializer
from django.contrib.auth.models import User


class BooksApiTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_username")
        self.book_1 = Book.objects.create(title='Test Book 1', price=25, author='Author 1', owner=self.user)
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

    @skip
    def test_get_filter(self):
        """тест: получение filter"""
        url = reverse("book-list")
        print(url)
        response = self.client.get(url, data={'price': 55})
        serializer_data = BookSerializer([self.book_1, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        """тест: получение search"""
        url = reverse("book-list")
        print(url)
        response = self.client.get(url, data={"search": "Author 1"})
        serializer_data = BookSerializer([self.book_1, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        """тест: создание объекта Book"""
        self.assertEqual(3, Book.objects.all().count())
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
        book_1 = Book.objects.get(id=4)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())
        self.assertEqual([data['title'], data['price'], data['author']], [book_1.title, book_1.price, book_1.author])
        self.assertEqual(self.user, Book.objects.last().owner)
        print(Book.objects.last().owner)

    def test_update(self):
        """тест: обновление объекта Book"""
        url = reverse("book-detail", args=(self.book_1.id,))
        data = {
            "title": self.book_1.title,
            "price": 575,
            "author": self.book_1.author,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        print(url)
        response = self.client.put(
            url, data=json_data, content_type="application/json"
        )
        # self.book_1 = Book.objects.get(id=self.book_1.id)
        self.book_1.refresh_from_db()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(575, self.book_1.price)

    def test_update_not_owner(self):
        """тест: обновление объекта Book без owner"""
        self.user2 = User.objects.create(username='test_username2',)
        url = reverse("book-detail", args=(self.book_1.id,))
        data = {
            "title": self.book_1.title,
            "price": 575,
            "author": self.book_1.author,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        print(url)
        response = self.client.put(
            url, data=json_data, content_type="application/json"
        )
        # self.book_1 = Book.objects.get(id=self.book_1.id)
        self.book_1.refresh_from_db()

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(25, self.book_1.price)
        self.assertEqual(
            {
                "detail": ErrorDetail(
                    string="You do not have permission to perform this action.",
                    code="permission_denied",
                )
            }, response.data
        )
        print(response.data)

    def test_update_not_owner_but_staff(self):
        """тест: обновление объекта Book без owner"""
        self.user2 = User.objects.create(
            username="test_username2", is_staff=True
        )
        url = reverse("book-detail", args=(self.book_1.id,))
        data = {
            "title": self.book_1.title,
            "price": 575,
            "author": self.book_1.author,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        print(url)
        response = self.client.put(url, data=json_data, content_type="application/json")
        self.book_1.refresh_from_db()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(575, self.book_1.price)


class BooksRelationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_username")
        self.user2 = User.objects.create(username="test_username2")
        self.book_1 = Book.objects.create(
            title="Test Book 1", price=25, author="Author 1", owner=self.user
        )
        self.book_2 = Book.objects.create(
            title="Test Book 2", price=55, author="Author 2"
        )

    def test_like(self):
        """тест: like"""
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))

        data = {
            "like": True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(
            url, data=json_data, content_type='application/json'
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user,
                                                book=self.book_1)
        self.book_1.refresh_from_db()
        self.assertTrue(relation.like)

        data = {
            "in_bookmarks": True,
        }
        json_data = json.dumps(data)
        response = self.client.patch(
            url, data=json_data, content_type="application/json"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user,
                                                book=self.book_1)
        self.assertTrue(relation.in_bookmarks)

    def test_rate(self):
        """тест: like"""
        url = reverse("userbookrelation-detail", args=(self.book_1.id,))

        data = {
            "rate": 3,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(
            url, data=json_data, content_type="application/json"
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.book_1.refresh_from_db()
        self.assertEqual(3, relation.rate)

    def test_rate_wrong(self):
        """тест: like"""
        url = reverse("userbookrelation-detail", args=(self.book_1.id,))

        data = {
            "rate": 6,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(
            url, data=json_data, content_type="application/json"
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.book_1.refresh_from_db()
        self.assertEqual(3, relation.rate)
