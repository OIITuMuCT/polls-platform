
from django.test import TestCase
from django.contrib.auth.models import User

from store.models import Book, UserBookRelation
from store.logic import set_rating

class SetRatingTest(TestCase):
    """ тест: проверка рейтинга"""
    def setUp(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username="user2")
        user3 = User.objects.create(username='user3')

        self.book_1 = Book.objects.create(title="Test Book 1", price=25,
                                        author='Author 1', owner=user1)

        UserBookRelation.objects.create(user=user1, book=self.book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=self.book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=user3, book=self.book_1, like=True, rate=4)

    def test_ok(self):
        set_rating(self.book_1)
        self.book_1.refresh_from_db()
        self.assertEqual('4.67', str(self.book_1.rating))

