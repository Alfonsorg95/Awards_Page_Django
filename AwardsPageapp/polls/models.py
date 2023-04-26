import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=100)
    publication_date = models.DateTimeField("Date published")

    def __str__(self) -> str:
        return self.question_text

    def was_published_recently(self):
        return self.publication_date >= timezone.now() - datetime.timedelta(days=7)


class Choice(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.choice_text
