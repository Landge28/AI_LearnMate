from .models import Notification

def notification_context(request):


    return {"notifications": Notification.objects.filter(is_active=True).order_by("-created_at")[:5]}