from __future__ import annotations

from django.conf import settings
from django.core.mail import send_mail


def send_notification_email(to_email: str, subject: str, body: str) -> bool:
    if not to_email or not str(to_email).strip():
        return False
    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            fail_silently=False,
        )
        return True
    except Exception:
        return False
