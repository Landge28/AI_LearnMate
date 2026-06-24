from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# ==========================================
# PROGRESS TRACKER MODEL
# Stores Student Learning Progress
# ==========================================
class ProgressTracker(models.Model):

    student = models.OneToOneField(User,on_delete=models.CASCADE)

    quizzes_attempted = models.IntegerField(default=0)

    average_score = models.FloatField(default=0)

    highest_score = models.IntegerField(default=0)

    progress_percentage = models.FloatField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.username