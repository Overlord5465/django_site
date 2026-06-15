from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta

from .models import Message
from .utils import chat_separator_date_label
from profiles.models import Student, Teacher
from django.contrib.auth import get_user_model

User = get_user_model()


def _teachers_in_user_department(user):
    qs = Teacher.objects.all()
    dept_id = getattr(getattr(user, "teacher", None), "department_id", None)
    if dept_id:
        qs = qs.filter(department_id=dept_id)
    return qs


def _mark_thread(user, other):
    now = timezone.now()
    Message.objects.filter(sender=other, recipient=user, delivered_at__isnull=True).update(delivered_at=now)
    Message.objects.filter(sender=other, recipient=user, read=False).update(read=True, read_at=now)


@login_required
def chat_room(request, recipient_id=None):
    user = request.user
    today = timezone.localdate()
    yesterday = today - timedelta(days=1)
    today_key = today.isoformat()
    yesterday_key = yesterday.isoformat()

    if hasattr(user, "student"):
        student = user.student
        if not student.scientific_director:
            return render(
                request,
                "chat/chat_room.html",
                {"chat_messages": None, "recipient": None, "students_list": None},
            )
        recipient = student.scientific_director.user
        _mark_thread(user, recipient)
        chat_messages = Message.objects.filter(
            Q(sender=user, recipient=recipient) | Q(sender=recipient, recipient=user)
        ).order_by("timestamp")
        students_list = None

    elif hasattr(user, "teacher"):
        if getattr(user, "user_type", None) == "department_admin":
            students_list = (
                Student.objects.filter(scientific_director__in=_teachers_in_user_department(user))
                .select_related("user")
                .order_by("user__first_name", "user__last_name", "user__username")
            )
        else:
            students_list = Student.objects.filter(scientific_director=user.teacher).select_related("user").order_by(
                "user__first_name", "user__last_name", "user__username"
            )
        if recipient_id:
            recipient = get_object_or_404(User, id=recipient_id)
            _mark_thread(user, recipient)
            chat_messages = Message.objects.filter(
                Q(sender=user, recipient=recipient) | Q(sender=recipient, recipient=user)
            ).order_by("timestamp")
        else:
            chat_messages = None
            recipient = None
    else:
        return render(
            request,
            "chat/chat_room.html",
            {"chat_messages": None, "recipient": None, "students_list": None},
        )

    return render(
        request,
        "chat/chat_room.html",
        {
            "chat_messages": chat_messages,
            "recipient": recipient,
            "students_list": students_list,
            "today_key": today_key,
            "yesterday_key": yesterday_key,
        },
    )


@require_POST
@login_required
def send_message(request):
    recipient_id = request.POST.get("recipient_id")
    content = request.POST.get("content") or ""
    attachment = request.FILES.get("attachment")

    if not recipient_id or (not content.strip() and not attachment):
        return JsonResponse({"status": "error", "message": "Missing data"})

    recipient = get_object_or_404(User, id=recipient_id)
    user = request.user

    if hasattr(user, "student"):
        if recipient != user.student.scientific_director.user:
            return JsonResponse({"status": "error", "message": "Permission denied"})

    elif hasattr(user, "teacher"):
        if getattr(user, "user_type", None) == "department_admin":
            tq = _teachers_in_user_department(user)
            if not Student.objects.filter(user=recipient, scientific_director__in=tq).exists():
                return JsonResponse({"status": "error", "message": "Permission denied"})
        else:
            if not Student.objects.filter(user=recipient, scientific_director=user.teacher).exists():
                return JsonResponse({"status": "error", "message": "Permission denied"})
    else:
        return JsonResponse({"status": "error", "message": "Permission denied"})

    message = Message.objects.create(
        sender=user,
        recipient=recipient,
        content=content,
        read=False,
        attachment=attachment or None,
    )

    msg_date = timezone.localtime(message.timestamp).date()
    today = timezone.localdate()
    date_key = msg_date.isoformat()
    if msg_date == today:
        date_label = "сегодня"
    elif msg_date == (today - timedelta(days=1)):
        date_label = "вчера"
    else:
        date_label = chat_separator_date_label(message.timestamp)

    payload = {
        "id": message.id,
        "content": message.content,
        "timestamp": message.timestamp.strftime("%H:%M"),
        "has_file": bool(message.attachment),
        "date_key": date_key,
        "date_label": date_label,
    }
    if message.attachment:
        payload["attachment_url"] = message.attachment.url
        payload["attachment_name"] = message.attachment_basename

    return JsonResponse(
        {
            "status": "success",
            "message": payload,
        }
    )
