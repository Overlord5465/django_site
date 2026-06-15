from __future__ import annotations

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from works.email import send_notification_email
from works.models import Notification, Work


class Command(BaseCommand):
    help = "Уведомления о давности последнего DOCX (7 дней — студент, 30 — руководитель)."

    def handle(self, *args, **options):
        now = timezone.now()
        n_st = 0
        n_t = 0
        for work in Work.objects.filter(status=Work.LifecycleStatus.NOT_READY).select_related(
            "author__user", "scientific_director__user"
        ):
            t = getattr(work, "docx_updated_at", None)
            if not t:
                continue
            age = now - t
            uf = []

            if age >= timedelta(days=7) and not work.student_docx_reminder_sent_at:
                st = work.author
                if st and st.user_id:
                    title = "Пора поработать над документом"
                    body = (
                        f"Последнее изменение файла работы «{work.name}» было более недели назад. "
                        f"Уделите время оформлению текста."
                    )
                    Notification.objects.create(recipient=st.user, title=title, body=body, url="/works/write_work/")
                    if getattr(st.user, "email", None):
                        send_notification_email(st.user.email, title, body)
                    work.student_docx_reminder_sent_at = now
                    uf.append("student_docx_reminder_sent_at")
                    n_st += 1

            if age >= timedelta(days=30) and not work.teacher_stale_docx_notified_at:
                teacher = work.scientific_director
                if teacher and teacher.user_id:
                    st = work.author
                    if st and st.user:
                        sn = st.user.get_full_name() or st.user.username
                    else:
                        sn = "Студент"
                    title = "Студент давно не редактировал работу"
                    body = f"{sn} — работа «{work.name}»: более 30 дней без изменений DOCX."
                    Notification.objects.create(
                        recipient=teacher.user,
                        title=title,
                        body=body,
                        url=f"/works/review_work/{work.id}/",
                    )
                    if getattr(teacher.user, "email", None):
                        send_notification_email(teacher.user.email, title, body)
                    work.teacher_stale_docx_notified_at = now
                    uf.append("teacher_stale_docx_notified_at")
                    n_t += 1

            if uf:
                work.save(update_fields=uf)

        self.stdout.write(self.style.SUCCESS(f"Студентам: {n_st}, преподавателям: {n_t}"))

