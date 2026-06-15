from __future__ import annotations

from django.db.models import F
from django.urls import reverse
from django.utils import timezone

from profiles.course_utils import student_course_bucket
from profiles.models import DirectionOfStudy, Student, Teacher
from profiles.seat_sync import ensure_teacher_seats
from works.models import Notification, StudentTopicProposal, Topic, TopicApplication


def notify(recipient, title: str, body: str = "", url: str = "") -> None:
    Notification.objects.create(recipient=recipient, title=title, body=body, url=url)


def user_display_name(user) -> str:
    return (user.get_full_name() or "").strip() or user.username


def has_available_seat(teacher: Teacher, student: Student) -> bool:
    from profiles.models import TeacherCourseSeat

    bucket = student_course_bucket(student)
    if not bucket:
        return True
    ensure_teacher_seats(teacher)
    rec = TeacherCourseSeat.objects.filter(teacher=teacher, bucket=bucket).first()
    if not rec:
        return True
    return rec.current_amount < rec.max_amount


def reject_other_pending_applications_for_topic(topic: Topic, approved_student_id: int) -> None:
    others = TopicApplication.objects.filter(topic=topic, status=TopicApplication.Status.PENDING).exclude(
        student_id=approved_student_id
    )
    now = timezone.now()
    for app in others:
        app.status = TopicApplication.Status.REJECTED
        app.decided_at = now
        app.save(update_fields=["status", "decided_at"])
        notify(
            app.student.user,
            "Отказ по заявке на тему",
            (
                f"Тема «{topic.title}» закреплена за другим студентом.\n"
                "Отказ сформирован автоматически после утверждения заявки другого студента."
            ),
            "",
        )


def reject_other_pending_for_student(student: Student, except_teacher_id: int) -> None:
    now = timezone.now()
    for app in TopicApplication.objects.filter(student=student, status=TopicApplication.Status.PENDING).select_related(
        "topic"
    ):
        if app.topic.creator_id != except_teacher_id:
            app.status = TopicApplication.Status.REJECTED
            app.decided_at = now
            app.save(update_fields=["status", "decided_at"])
            notify(
                student.user,
                "Отказ по заявке на тему",
                (
                    f"Вы выбрали другого научного руководителя. Заявка: «{app.topic.title}»\n"
                    "Отказ сформирован автоматически после закрепления за другим руководителем."
                ),
                "",
            )
    for prop in StudentTopicProposal.objects.filter(student=student, status=StudentTopicProposal.Status.PENDING):
        if prop.teacher_id != except_teacher_id:
            prop.status = StudentTopicProposal.Status.REJECTED
            prop.decided_at = now
            prop.save(update_fields=["status", "decided_at"])
            notify(
                student.user,
                "Отказ по предложенной теме",
                (
                    f"Вы закреплены за другим преподавателем. Тема: «{prop.title}»\n"
                    "Отказ сформирован автоматически после закрепления за другим руководителем."
                ),
                "",
            )


def reject_pending_when_no_seats(teacher: Teacher, bucket: str | None) -> None:
    """Отклоняет ожидающие заявки, если по корзине курса мест нет."""
    from profiles.models import TeacherCourseSeat

    if not bucket:
        return
    ensure_teacher_seats(teacher)
    rec = TeacherCourseSeat.objects.filter(teacher=teacher, bucket=bucket).first()
    if not rec or rec.current_amount < rec.max_amount:
        return
    now = timezone.now()
    for app in TopicApplication.objects.filter(
        status=TopicApplication.Status.PENDING,
        topic__creator=teacher,
    ).select_related("student__user", "student__group__direction_of_study", "topic"):
        if student_course_bucket(app.student) != bucket:
            continue
        app.status = TopicApplication.Status.REJECTED
        app.decided_at = now
        app.save(update_fields=["status", "decided_at"])
        notify(
            app.student.user,
            "Отказ по заявке",
            (
                "У преподавателя нет свободных мест по вашему курсу. "
                f"Тема: «{app.topic.title}»\nПреподаватель: {user_display_name(teacher.user)}."
            ),
            "",
        )
    for prop in StudentTopicProposal.objects.filter(
        status=StudentTopicProposal.Status.PENDING,
        teacher=teacher,
    ).select_related("student__user", "student__group__direction_of_study"):
        if student_course_bucket(prop.student) != bucket:
            continue
        prop.status = StudentTopicProposal.Status.REJECTED
        prop.decided_at = now
        prop.save(update_fields=["status", "decided_at"])
        notify(
            prop.student.user,
            "Отказ по предложенной теме",
            (
                "У преподавателя нет свободных мест по вашему курсу. "
                f"Тема: «{prop.title}»\nПреподаватель: {user_display_name(teacher.user)}."
            ),
            "",
        )


def allowed_topic_work_kinds_for_student(student: Student) -> list[str] | None:
    """None — без ограничений, иначе допустимые Topic.work_kind."""
    if not student.group or not student.group.direction_of_study:
        return None
    dos = student.group.direction_of_study
    if dos.level_of_training == DirectionOfStudy.MASTERS_DEGREE:
        return [Topic.WorkKind.MASTER]
    c = getattr(student.group, "course", None)
    if c == 3:
        return [Topic.WorkKind.COURSEWORK]
    if c == 4:
        return [Topic.WorkKind.BACHELOR]
    return [Topic.WorkKind.COURSEWORK, Topic.WorkKind.BACHELOR]


def filter_topic_bank_for_student_capacity(qs, student: Student):
    bucket = student_course_bucket(student)
    if not bucket:
        return qs
    from profiles.models import TeacherCourseSeat

    full_teacher_ids = TeacherCourseSeat.objects.filter(bucket=bucket).filter(
        current_amount__gte=F("max_amount")
    ).values_list("teacher_id", flat=True)
    bucket_work_kinds = {
        "b3": [Topic.WorkKind.COURSEWORK],
        "b4": [Topic.WorkKind.BACHELOR],
        "m1": [Topic.WorkKind.MASTER],
        "m2": [Topic.WorkKind.MASTER],
    }.get(bucket, None)
    if bucket_work_kinds is None:
        return qs.exclude(creator_id__in=full_teacher_ids)
    return qs.exclude(creator_id__in=full_teacher_ids, work_kind__in=bucket_work_kinds)
