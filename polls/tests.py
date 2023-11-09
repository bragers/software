from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Question


class QuestionModelTest(TestCase):
    def test_create_question(self):
        # Create a new question with a past pub_date
        pub_date = timezone.now() - timezone.timedelta(days=1)
        question = Question(
            question_text="What's your favorite place",
            pub_date=pub_date,
            for_kids=False,
            high_activity=True,
        )
        question.save()

        # Retrieve the question from the database
        saved_question = Question.objects.get(pk=question.pk)

        # Check if the retrieved question matches the created one
        self.assertEqual(saved_question.question_text, "What's your favorite place")
        self.assertEqual(saved_question.for_kids, False)
        self.assertEqual(saved_question.high_activity, True)

    def test_pub_date_in_past(self):
        # Attempt to create a question with a pub_date in the past
        pub_date_past = timezone.now() - timezone.timedelta(days=1)
        question = Question(
            question_text="What's your favorite place",
            pub_date=pub_date_past,
            for_kids=False,
            high_activity=True,
        )
        question.save()


class QuestionViewTest(TestCase):
    def test_question_detail_view(self):
        # Create a sample question
        question = Question.objects.create(
            question_text="Sample Question",
            pub_date=timezone.now(),
            for_kids=True,
            high_activity=False,
        )

        # Test the question detail view
        response = self.client.get(reverse('polls:question_detail', args=(question.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Question")

