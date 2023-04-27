import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse

from .models import Question


def create_question(question_text, days):
    """Creates a question with the given question text, and the publication date offset from now
    negative numbers will give dates in the past and positive numbers will give dates n the future
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, publication_date=time)


class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions published in the future"""
        self.question = create_question("future question", 15)
        self.assertIs(self.question.was_published_recently(), False)

    def test_was_published_recently_with_question_in_the_past_week(self):
        """was_published_recently returns True for questions published in the last 7 days"""
        self.question = create_question("present question", -2)
        self.assertIs(self.question.was_published_recently(), True)

    def test_was_published_recently_with_questions_with_more_than_a_week(self):
        """was_published_recently returns False for questions published more than 7 days ago"""
        self.question = create_question("past question", -15)
        self.assertIs(self.question.was_published_recently(), False)


class QuestionIndexView(TestCase):
    def test_no_questions(self):
        """If no question exist, an apropiate message is dilplayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_no_future_questions_on_the_list(self):
        """Index view doesn't show questions with a future publication date"""
        create_question("Future question", 15)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with publication date in the past are displayed
        """
        question = create_question("Old question", -15)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

    def test_no_more_than_5_past_questions(self):
        """
        Index page shows a maximum of five questions
        """
        [create_question(f"Question {i}", -i) for i in range(0, 8)]
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["latest_question_list"]), 5)


class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        """
        Detail view is no available for future questions
        """
        future_question = create_question("Future question", 15)
        url = reverse("polls:detail", args=(future_question.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_questions(self):
        """
        Detail view displays past questions
        """
        past_question = create_question("Past question", -15)
        url = reverse("polls:detail", args=(past_question.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)
