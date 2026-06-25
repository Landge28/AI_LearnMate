from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Recommendation

# ==========================================
# RECOMMENDATION ADMIN CONFIGURATION
# Registers recommendation models
# in Django Admin Panel
# ==========================================


admin.site.register(Recommendation)