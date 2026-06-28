from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class StudyPlan(models.Model):

    student = models.ForeignKey(User,on_delete=models.CASCADE,related_name="study_plans")

    title = models.CharField(max_length=200)

    description = models.TextField()

    day_number = models.IntegerField()

    estimated_minutes = models.IntegerField()

    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["day_number"]

    def __str__(self):
        return f"Day {self.day_number} - {self.student.username}"