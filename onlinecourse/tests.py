from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from onlinecourse.models import Course, Lesson, Question, Choice, Enrollment, Submission


class OnlineCourseExamTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='teststudent', password='password123', first_name='Harshit')
        self.client.login(username='teststudent', password='password123')

        self.course = Course.objects.create(name="Python Fundamentals", description="Test Course")
        self.lesson = Lesson.objects.create(title="Lesson 1", content="Intro", course=self.course, order=0)
        self.enrollment = Enrollment.objects.create(user=self.user, course=self.course)

        # Q1
        self.q1 = Question.objects.create(course=self.course, question_text="What is 2+2?", grade=50)
        self.q1_c1 = Choice.objects.create(question=self.q1, choice_text="4", is_correct=True)
        self.q1_c2 = Choice.objects.create(question=self.q1, choice_text="5", is_correct=False)

        # Q2
        self.q2 = Question.objects.create(course=self.course, question_text="Is Python dynamic?", grade=50)
        self.q2_c1 = Choice.objects.create(question=self.q2, choice_text="Yes", is_correct=True)
        self.q2_c2 = Choice.objects.create(question=self.q2, choice_text="No", is_correct=False)

    def test_course_details_view(self):
        url = reverse('onlinecourse:course_details', args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Fundamentals")
        self.assertContains(response, "Lesson 1")
        self.assertContains(response, "Start Exam")

    def test_perfect_score_submission(self):
        url = reverse('onlinecourse:submit', args=[self.course.id])
        data = {
            f'choice_{self.q1_c1.id}': self.q1_c1.id,
            f'choice_{self.q2_c1.id}': self.q2_c1.id,
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Congratulations")
        self.assertContains(response, "100 / 100")
        self.assertContains(response, "100%")

        submission = Submission.objects.last()
        self.assertEqual(submission.choices.count(), 2)

    def test_partial_score_submission(self):
        url = reverse('onlinecourse:submit', args=[self.course.id])
        data = {
            f'choice_{self.q1_c1.id}': self.q1_c1.id,
            f'choice_{self.q2_c2.id}': self.q2_c2.id,  # wrong choice
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Congratulations")
        self.assertContains(response, "50 / 100")
        self.assertContains(response, "50%")
