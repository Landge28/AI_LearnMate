from django.db import models

# Create your models here.
from django.db import models

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