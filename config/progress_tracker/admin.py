from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ProgressTracker


# ==========================================
# PROGRESS TRACKER ADMIN CONFIGURATION
# Registers ProgressTracker Model
# in Django Admin Panel
# ==========================================
admin.site.register(ProgressTracker)