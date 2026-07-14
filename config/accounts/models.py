from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User




class Notification(models.Model):

    title = models.CharField(max_length=200)

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):

        return self.title
class StudentProfile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)

    profile_image = models.ImageField(
        upload_to="profile_images/",
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    location = models.CharField(
        max_length=100,
        blank=True
    )

    bio = models.TextField(
        blank=True
    )

    learning_goal = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return self.user.username