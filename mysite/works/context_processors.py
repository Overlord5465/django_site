from works.models import Notification


def unread_notifications(request):
    if request.user.is_authenticated:
        n = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return {"unread_notifications_count": n}
    return {"unread_notifications_count": 0}
