from accounts.models import Notification

def admin_notifications(request):

    return {"admin_notifications": Notification.objects.filter(is_active=True).order_by("-created_at")[:5]}