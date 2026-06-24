from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Quiz, Question, StudentResult

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(StudentResult)