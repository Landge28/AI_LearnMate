from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


# ============================================
# AI Tutor Models
# Stores AI conversation history
# ============================================
class ChatSession(models.Model):

    student = models.ForeignKey(User,on_delete=models.CASCADE,related_name="chat_sessions")

    title = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ChatMessage(models.Model):

    ROLE_CHOICES = (
        ("user", "User"),
        ("assistant", "Assistant"),
    )

    session = models.ForeignKey(ChatSession,on_delete=models.CASCADE,related_name="messages")

    role = models.CharField(max_length=20,choices=ROLE_CHOICES)

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} - {self.session.title}"




