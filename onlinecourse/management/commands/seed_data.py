from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.contrib.auth.models import User
from onlinecourse.models import Course, Lesson, Question, Choice, Instructor, Learner, Enrollment


class Command(BaseCommand):
    help = 'Seeds initial course, lessons, questions, and choices into the database without duplicating.'

    def handle(self, *args, **options):
        # Admin / Test user
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com', 'first_name': 'Admin', 'last_name': 'User', 'is_staff': True, 'is_superuser': True}
        )
        if not admin_user.has_usable_password():
            admin_user.set_password('admin12345')
            admin_user.save()

        # Student user
        student_user, _ = User.objects.get_or_create(
            username='student',
            defaults={'email': 'student@example.com', 'first_name': 'Harshit', 'last_name': 'Jain'}
        )
        if not student_user.has_usable_password():
            student_user.set_password('student12345')
            student_user.save()

        instructor, _ = Instructor.objects.get_or_create(
            user=admin_user,
            defaults={'full_time': True, 'total_learners': 100}
        )

        course, created = Course.objects.get_or_create(
            name='Python Fundamentals',
            defaults={
                'description': 'Master the core concepts of Python programming, including variables, control flow, functions, and data structures.',
                'pub_date': now().date(),
                'total_enrollment': 1
            }
        )
        course.instructors.add(instructor)

        # Enroll student in course
        Enrollment.objects.get_or_create(
            user=student_user,
            course=course,
            defaults={'mode': 'honor'}
        )
        Enrollment.objects.get_or_create(
            user=admin_user,
            course=course,
            defaults={'mode': 'honor'}
        )

        # Seed 3 Lessons
        lessons_data = [
            {
                'title': 'Introduction to Python & Variables',
                'order': 0,
                'content': 'Python is an interpreted, high-level, general-purpose programming language. Variables in Python are dynamically typed.'
            },
            {
                'title': 'Control Flow & Loops',
                'order': 1,
                'content': 'Control structures allow decisions and repetition. Python supports if-elif-else statements, for loops over iterables, and while loops.'
            },
            {
                'title': 'Functions & Data Structures',
                'order': 2,
                'content': 'Functions are defined using the def keyword and support default arguments, *args, and **kwargs. Built-in structures include lists, tuples, and dicts.'
            }
        ]

        for l_data in lessons_data:
            Lesson.objects.get_or_create(
                course=course,
                title=l_data['title'],
                defaults={'order': l_data['order'], 'content': l_data['content']}
            )

        # Seed 3 Questions with Choices
        questions_data = [
            {
                'question_text': 'What is the correct syntax to output "Hello World" in Python 3?',
                'grade': 50,
                'choices': [
                    {'text': 'print("Hello World")', 'is_correct': True},
                    {'text': 'echo "Hello World"', 'is_correct': False},
                    {'text': 'System.out.println("Hello World");', 'is_correct': False},
                ]
            },
            {
                'question_text': 'Which of the following data types in Python is immutable?',
                'grade': 50,
                'choices': [
                    {'text': 'list', 'is_correct': False},
                    {'text': 'tuple', 'is_correct': True},
                    {'text': 'dict', 'is_correct': False},
                ]
            },
            {
                'question_text': 'Which keyword is used to define a function in Python?',
                'grade': 50,
                'choices': [
                    {'text': 'function', 'is_correct': False},
                    {'text': 'def', 'is_correct': True},
                    {'text': 'func', 'is_correct': False},
                ]
            }
        ]

        for q_data in questions_data:
            question, _ = Question.objects.get_or_create(
                course=course,
                question_text=q_data['question_text'],
                defaults={'grade': q_data['grade']}
            )
            for c_data in q_data['choices']:
                Choice.objects.get_or_create(
                    question=question,
                    choice_text=c_data['text'],
                    defaults={'is_correct': c_data['is_correct']}
                )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully for tfjzl-final-cloud-app-with-database!"))

