from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Course, StudyMaterial
from .models import Certificate

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(StudyMaterial)
admin.site.register(Certificate)