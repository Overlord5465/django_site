from __future__ import annotations

from django.core.management.base import BaseCommand
from django.utils import timezone

from works.email import send_notification_email
from works.models import Notification, PlanStage, Work


class Command(BaseCommand):
    help = "Create notifications for overdue plan stages (once per stage)."

    def handle(self, *args, **options):
        today = timezone.localdate()
        now = timezone.now()

        qs = (
            PlanStage.objects.filter(
                due_date__isnull=False,
                due_date__lt=today,
                is_done=False,
                overdue_notified_at__isnull=True,
            )
            .exclude(plan__work__status=Work.LifecycleStatus.DEFENDED)
            .select_related("plan__work__scientific_director__user", "plan__work__author__user")
            .order_by("due_date")
        )

        created = 0
        for stage in qs:
            work = stage.plan.work
            teacher_user = getattr(getattr(work, "scientific_director", None), "user", None)
            if not teacher_user:
                stage.overdue_notified_at = now
                stage.save(update_fields=["overdue_notified_at"])
                continue

            student_user = getattr(getattr(work, "author", None), "user", None)
            student_name = student_user.get_full_name() if student_user else "Студент"

            body = f"{student_name}: {stage.title}"
            Notification.objects.create(
                recipient=teacher_user,
                title="Просрочен этап плана",
                body=body,
                url=f"/works/work/{work.id}/plan/",
            )
            if getattr(teacher_user, "email", None):
                send_notification_email(
                    teacher_user.email,
                    "Просрочен этап плана",
                    body + f"\n{work.name}\nОткройте: уведомления на сайте.",
                )

            stage.overdue_notified_at = now
            stage.save(update_fields=["overdue_notified_at"])
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} overdue notifications"))

