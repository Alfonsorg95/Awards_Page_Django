import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTest(TestCase):
    def setUp(self) -> None:
        self.question = Question(question_text="Is this test working?")

    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions published in the future"""
        time = timezone.now() + datetime.timedelta(days=15)
        self.question.publication_date = time
        self.assertIs(self.question.was_published_recently(), False)

    def test_was_published_recently_with_question_in_the_past_week(self):
        """was_published_recently returns True for questions published in the last 7 days"""
        time = timezone.now() - datetime.timedelta(days=1)
        self.question.publication_date = time
        self.assertIs(self.question.was_published_recently(), True)

    def test_was_published_recently_with_questions_with_more_than_a_week(self):
        """was_published_recently returns False for questions published more than 7 days ago"""
        time = timezone.now() - datetime.timedelta(days=15)
        self.question.publication_date = time
        self.assertIs(self.question.was_published_recently(), False)
