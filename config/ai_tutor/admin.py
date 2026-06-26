from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ChatSession, ChatMessage

admin.site.register(ChatSession)
admin.site.register(ChatMessage)