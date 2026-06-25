from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

# ==========================================
# RECOMMENDATION MODEL
# Stores AI-generated course recommendations
# for each student
# ==========================================
class Recommendation(models.Model):

    student = models.ForeignKey(User,on_delete=models.CASCADE)

    course = models.ForeignKey(Course,on_delete=models.CASCADE)

    reason = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} -> {self.course.title}"