# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# from config.courses.models import Course
from courses.models import Course

# ==========================================
# QUIZ MODEL
# Stores quiz information related to a course
# ==========================================
class Quiz(models.Model):

    course = models.ForeignKey(Course,on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    total_marks = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ==========================================
# QUESTION MODEL
# Stores questions related to a quiz
# ==========================================
class Question(models.Model):

    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)

    question_text = models.TextField()

    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    correct_answer = models.CharField(max_length=1,choices=[
            ('A', 'Option A'),
            ('B', 'Option B'),
            ('C', 'Option C'),
            ('D', 'Option D')
        ]
    )

    def __str__(self):
        return self.question_text


# ==========================================
# STUDENT RESULT MODEL
# Stores quiz results of students
# ==========================================
class StudentResult(models.Model):

    student = models.ForeignKey(User,on_delete=models.CASCADE)

    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)

    score = models.IntegerField()

    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.score}"