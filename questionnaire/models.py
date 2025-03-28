from django.db import models

# Create your models here.
class Question(models.Model):
    """ Модель вопроса для анкеты """
    QUESTION_LIST = {1: 'value 1', 2: 'value 2', 3: 'value 3', 4: 'value 4'}
    title = models.CharField(max_length=250)
    text = models.TextField()
    answer_option = models.CharField(max_length=4, choices=QUESTION_LIST)


class Polls(models.Model):
    """Модель Опроса"""
    title = models.CharField(max_length=250)
    description = models.TextField()
    question_list = models.ForeignKey(Question, on_delete=models.CASCADE)