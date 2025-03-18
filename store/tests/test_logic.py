from store.logic import operations
from django.test import TestCase

class LogicTest(TestCase):
    """ тест: проверка логики """
    def test_plus(self):
        """ тест сложение """
        result = operations(7, 13, '+')
        self.assertEqual(20, result)

    def test_minus(self):
        """ тест разность """
        result = operations(7, 13, '-')
        self.assertEqual(-6, result)
    def test_multiple(self):
        """ тест произведение """
        result = operations(5, 15, '*')
        self.assertEqual(75, result)
