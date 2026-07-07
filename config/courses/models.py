from django.db import models

# Create your models here.
from django.db import models

from django.contrib.auth.models import User
import uuid

# ==========================================
# CATEGORY MODEL
# Stores course categories
# Example:
# Python, Java, Cyber Security, AI
# ==========================================
class Category(models.Model):

    name = models.CharField(max_length=100,unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ==========================================
# COURSE MODEL
# Stores course information
# ==========================================
class Course(models.Model):

    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='courses')

    title = models.CharField(max_length=200)

    description = models.TextField()

    duration = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ==========================================
# STUDY MATERIAL MODEL
# Stores PDFs and Video Resources
# related to a course
# ==========================================
class StudyMaterial(models.Model):

    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='materials')

    title = models.CharField(max_length=200)

    pdf_file = models.FileField(upload_to='study_materials/',blank=True,null=True)

    video_url = models.URLField(blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Certificate(models.Model):

    student = models.ForeignKey(User,on_delete=models.CASCADE)

    course = models.ForeignKey(Course,on_delete=models.CASCADE)

    certificate_id = models.CharField(max_length=50,unique=True,editable=False)

    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")

    def save(self, *args, **kwargs):

        if not self.certificate_id:

            self.certificate_id = (
                f"ALM-{uuid.uuid4().hex[:10].upper()}"
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return self.certificate_id