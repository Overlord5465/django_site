from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils import timezone

from profiles.models import Student, Teacher


class Tag(models.Model):
    """Теги для фильтрации работ в архиве."""

    name = models.CharField(max_length=64, unique=True, db_index=True, verbose_name="Название")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Work(models.Model):
    class LifecycleStatus(models.TextChoices):
        NOT_READY = "not_ready", "Работа не готова"
        READY = "ready", "Работа готова (ожидает нормоконтроль)"
        NORM_OK = "norm_ok", "Нормоконтроль пройден"
        DEFENDED = "defended", "Работа защищена (архив)"

    name = models.CharField(max_length=200, db_index=True, verbose_name="Тема")
    description = models.TextField(blank=True, default="", verbose_name="Описание")
    type_of_work = models.CharField(max_length=100, blank=True, default="", verbose_name="Тип работы")

    created_at = models.DateTimeField(default=timezone.now, verbose_name="Создано", db_index=True)
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Завершено")

    author = models.ForeignKey(
        Student,
        verbose_name="Автор",
        on_delete=models.SET_NULL,
        null=True,
        related_name="works",
    )
    scientific_director = models.ForeignKey(
        Teacher,
        related_name="works",
        verbose_name="Научный руководитель",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=16,
        choices=LifecycleStatus.choices,
        default=LifecycleStatus.NOT_READY,
        db_index=True,
        verbose_name="Статус",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="works", verbose_name="Теги")

    student_docx_reminder_sent_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Напоминание студенту о неактивности DOCX"
    )
    teacher_stale_docx_notified_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Уведомление руководителю о месяце без правок"
    )

    # Одна актуальная копия DOCX на работу (без истории версий).
    docx_file = models.FileField(upload_to="work_docs/", blank=True, null=True)
    # Нужно для проверки неактивности (неделя/месяц без изменений DOCX).
    docx_updated_at = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        verbose_name = "Работа"
        verbose_name_plural = "Работы"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        """При смене DOCX обновляем docx_updated_at — иначе OnlyOffice держит старый документ по тому же key."""
        if self.pk:
            old = (
                Work.objects.filter(pk=self.pk)
                .only("docx_file")
                .first()
            )
            if old is not None:
                prev = (old.docx_file.name or "") if old.docx_file else ""
                new = (self.docx_file.name or "") if self.docx_file else ""
                if prev != new:
                    self.docx_updated_at = timezone.now()
        elif self.docx_file:
            self.docx_updated_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def is_archived(self) -> bool:
        return self.status == self.LifecycleStatus.DEFENDED

    @property
    def is_ready_for_norm(self) -> bool:
        return self.status in (self.LifecycleStatus.READY, self.LifecycleStatus.NORM_OK, self.LifecycleStatus.DEFENDED)

    @property
    def is_norm_passed(self) -> bool:
        return self.status in (self.LifecycleStatus.NORM_OK, self.LifecycleStatus.DEFENDED)


class Topic(models.Model):
    """Банк тем, созданных преподавателями."""

    class WorkKind(models.TextChoices):
        COURSEWORK = "coursework", "Курсовая работа"
        BACHELOR = "bachelor", "ВКР (бакалавриат)"
        MASTER = "master", "Магистерская диссертация"

    creator = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name="topics", verbose_name="Автор (преподаватель)"
    )
    title = models.CharField(max_length=200, db_index=True, verbose_name="Название темы")
    description = models.TextField(blank=True, default="", verbose_name="Описание")
    work_kind = models.CharField(
        max_length=32,
        choices=WorkKind.choices,
        default=WorkKind.BACHELOR,
        db_index=True,
        verbose_name="Тип работы",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = "Тема (банк)"
        verbose_name_plural = "Темы (банк)"

    def __str__(self) -> str:
        return self.title


class TopicApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Ожидает"
        APPROVED = "approved", "Утверждена"
        REJECTED = "rejected", "Отклонена"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="topic_applications")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    decided_at = models.DateTimeField(null=True, blank=True)
    decision_comment = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = "Заявка на тему"
        verbose_name_plural = "Заявки на темы"
        constraints = [
            models.UniqueConstraint(fields=["student", "topic"], name="uniq_student_topic_application"),
        ]


class StudentTopicProposal(models.Model):
    """Студент предлагает свою тему конкретному преподавателю."""

    class Status(models.TextChoices):
        PENDING = "pending", "Ожидает"
        APPROVED = "approved", "Утверждена"
        REJECTED = "rejected", "Отклонена"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="topic_proposals")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="topic_proposals")
    title = models.CharField(max_length=200, verbose_name="Тема")
    description = models.TextField(blank=True, default="", verbose_name="Описание работы")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    decided_at = models.DateTimeField(null=True, blank=True)
    decision_comment = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = "Предложение темы студентом"
        verbose_name_plural = "Предложения тем студентами"


class Notification(models.Model):
    """Лента уведомлений об изменении статусов (заявки на темы, планы, рецензии)."""

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_read = models.BooleanField(default=False, db_index=True)
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True, default="")
    url = models.CharField(max_length=300, blank=True, default="")

    class Meta:
        ordering = ("-created_at",)


class IndividualPlan(models.Model):
    work = models.OneToOneField(Work, on_delete=models.CASCADE, related_name="plan")
    created_at = models.DateTimeField(auto_now_add=True)


class PlanStage(models.Model):
    plan = models.ForeignKey(IndividualPlan, on_delete=models.CASCADE, related_name="stages")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    title = models.CharField(max_length=200)
    due_date = models.DateField(null=True, blank=True)
    student_ready = models.BooleanField(default=False, db_index=True)
    ready_at = models.DateTimeField(null=True, blank=True)
    is_done = models.BooleanField(default=False, db_index=True)
    done_at = models.DateTimeField(null=True, blank=True)
    overdue_notified_at = models.DateTimeField(null=True, blank=True, db_index=True)
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ("order", "id")
