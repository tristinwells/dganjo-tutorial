

# Create your tests here.
import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for questions whose
        pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(), True)

    def test_add_question(self):
        """
        test_add_pull should return true if a poll was successfully created
        """
        question = Question.objects.create(
            question_text='What is your name?',
            pub_date=datetime.datetime.utcnow()
        )

        db_question = Question.objects.get(id=question.id)
        self.assertEqual(question, db_question)

    def test_edit_question(self):
        """
        Test that editing the poll was successful
        """
        # create the initial object
        question = Question.objects.create(
            question_text='What is your name?',
            pub_date=datetime.datetime.utcnow()
        )

        # make a change
        change_text = 'What is up?'
        question.question_text = change_text
        question.save()

        # get the object from the database
        db_question = Question.objects.get(id=question.id)
        self.assertEqual(db_question.question_text, change_text)

    def test_delete_question(self):
        """
        test_delete_poll should test if a poll is deleted that it no longer
        exists in the database
        """
        question = Question.objects.create(
            question_text='What is your name?',
            pub_date=datetime.datetime.utcnow()
        )

        question_id = question.id
        question.delete()

        db_question = Question.objects.filter(id=question_id)
        self.assertEqual(len(db_question), 0)
