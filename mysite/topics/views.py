from __future__ import annotations

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from profiles.course_utils import student_course_bucket
from profiles.models import Teacher
from profiles.seat_sync import sync_teacher_course_counts
from topics.forms import (
    DepartmentTopicForm,
    ProposeTopicForm,
    StudentTopicProposalDecisionForm,
    TopicApplicationDecisionForm,
    TopicForm,
)
from topics.services import (
    allowed_topic_work_kinds_for_student,
    filter_topic_bank_for_student_capacity,
    has_available_seat,
    notify,
    reject_other_pending_applications_for_topic,
    reject_other_pending_for_student,
    reject_pending_when_no_seats,
    user_display_name,
)
from users.rbac import require_user_types
from works.models import StudentTopicProposal, Topic, TopicApplication, Work
from works.student_work_type import type_of_work_label_for_student
from works.views import _ensure_work_document, _generate_initial_docx


def topic_bank(request):
    qs = Topic.objects.filter(is_active=True).select_related("creator__user").order_by("work_kind", "-created_at")
    ut = getattr(request.user, "user_type", None)
    if ut == "department_admin":
        dept_id = getattr(getattr(request.user, "teacher", None), "department_id", None)
        if dept_id:
            qs = qs.filter(creator__department_id=dept_id)
    if ut == "student" and hasattr(request.user, "student"):
        st = request.user.student
        kinds = allowed_topic_work_kinds_for_student(st)
        if kinds is not None:
            qs = qs.filter(work_kind__in=kinds)
        qs = filter_topic_bank_for_student_capacity(qs, st)
    can_apply = False
    can_propose = False
    if ut == "student" and hasattr(request.user, "student"):
        st = request.user.student
        can_apply = st.scientific_director_id is None
        can_propose = st.scientific_director_id is None
    return render(
        request,
        "works/topic_bank.html",
        {
            "topics": qs,
            "can_apply": can_apply,
            "can_propose": can_propose,
            "topic_work_kinds": Topic.WorkKind,
        },
    )


@require_user_types("student")
def propose_topic(request):
    student = request.user.student
    if student.scientific_director_id:
        messages.warning(request, "У вас уже есть научный руководитель.")
        return redirect("topic_bank")
    if request.method == "POST":
        form = ProposeTopicForm(request.POST)
        if form.is_valid():
            teacher = form.cleaned_data["teacher"]
            if StudentTopicProposal.objects.filter(
                student=student, teacher=teacher, status=StudentTopicProposal.Status.PENDING
            ).exists():
                messages.info(request, "У вас уже есть ожидающее предложение этому преподавателю.")
                return redirect("topic_bank")
            prop = StudentTopicProposal.objects.create(
                student=student,
                teacher=teacher,
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
            )
            teacher_name = user_display_name(teacher.user)
            notify(
                teacher.user,
                "Предложение темы от студента",
                f"{student.user.get_full_name() or student.user.username}: {prop.title}",
                "",
            )
            notify(
                student.user,
                "Заявка на тему на рассмотрении",
                f"Ваша заявка на тему «{prop.title}» у преподавателя {teacher_name} находится на рассмотрении.",
                reverse("notifications"),
            )
            messages.success(request, "Предложение отправлено. Преподаватель получит уведомление.")
            return redirect("topic_bank")
    else:
        form = ProposeTopicForm()
    return render(request, "works/propose_topic.html", {"form": form})


@require_user_types("teacher", "department_admin")
def create_topic(request):
    if getattr(request.user, "user_type", None) == "teacher":
        teacher = request.user.teacher
        if request.method == "POST":
            form = TopicForm(request.POST)
            if form.is_valid():
                t = form.save(commit=False)
                t.creator = teacher
                t.is_active = True
                t.save()
                return redirect("topic_bank")
        else:
            form = TopicForm()
        return render(request, "works/topic_form.html", {"form": form})

    teacher_qs = Teacher.objects.select_related("user").order_by("user__first_name")
    dept_id = getattr(getattr(request.user, "teacher", None), "department_id", None)
    if dept_id:
        teacher_qs = teacher_qs.filter(department_id=dept_id)
    if request.method == "POST":
        form = DepartmentTopicForm(request.POST, teacher_qs=teacher_qs)
        if form.is_valid():
            t = form.save(commit=False)
            t.creator = form.cleaned_data["teacher"]
            t.is_active = True
            t.save()
            return redirect("topic_bank")
    else:
        form = DepartmentTopicForm(teacher_qs=teacher_qs)
    return render(request, "works/topic_form.html", {"form": form, "is_department_admin": True})


@require_POST
@require_user_types("student")
def apply_topic(request, topic_id: int):
    topic = get_object_or_404(Topic, id=topic_id, is_active=True)
    student = request.user.student
    allowed = allowed_topic_work_kinds_for_student(student)
    if allowed is not None and topic.work_kind not in allowed:
        messages.error(request, "Эта тема не соответствует вашему курсу или уровню подготовки.")
        return redirect("topic_bank")
    app, created = TopicApplication.objects.get_or_create(student=student, topic=topic)
    if created:
        stud_name = user_display_name(student.user)
        teacher_user = topic.creator.user
        teacher_name = user_display_name(teacher_user)
        t_title = topic.title
        notify(
            teacher_user,
            "Заявка студента на рассмотрении",
            (
                f"Студент {stud_name} подал заявку на тему «{t_title}». Заявка находится на рассмотрении.\n"
                f"Преподаватель (автор темы в банке): {teacher_name}."
            ),
            reverse("topic_applications"),
        )
        notify(
            student.user,
            "Заявка на тему на рассмотрении",
            f"Ваша заявка на тему «{t_title}» у преподавателя {teacher_name} находится на рассмотрении.",
            reverse("notifications"),
        )
        messages.success(
            request,
            "Заявка успешно отправлена. После ответа преподавателя вы получите уведомление в разделе «Уведомления».",
        )
    else:
        messages.info(request, "Вы уже подавали заявку на эту тему.")
    return redirect("topic_bank")


@require_user_types("teacher", "department_admin")
def topic_applications(request):
    if request.user.user_type == "teacher":
        apps = TopicApplication.objects.filter(topic__creator=request.user.teacher).select_related(
            "student__user", "student__group__direction_of_study", "topic"
        )
        proposals = StudentTopicProposal.objects.filter(teacher=request.user.teacher).select_related(
            "student__user", "student__group__direction_of_study"
        )
    else:
        apps = TopicApplication.objects.all().select_related(
            "student__user", "student__group__direction_of_study", "topic", "topic__creator__user"
        )
        proposals = StudentTopicProposal.objects.select_related(
            "student__user", "student__group__direction_of_study", "teacher__user"
        )
        dept_id = getattr(getattr(request.user, "teacher", None), "department_id", None)
        if dept_id:
            apps = apps.filter(topic__creator__department_id=dept_id)
            proposals = proposals.filter(teacher__department_id=dept_id)
    return render(request, "works/topic_applications.html", {"applications": apps, "proposals": proposals})


@require_user_types("teacher", "department_admin")
def decide_topic_application(request, application_id: int):
    app = get_object_or_404(TopicApplication, id=application_id)
    if request.user.user_type == "teacher" and app.topic.creator_id != request.user.teacher.id:
        return redirect("topic_applications")
    if request.user.user_type == "department_admin":
        dept_id = getattr(getattr(request.user, "teacher", None), "department_id", None)
        if dept_id and app.topic.creator.department_id != dept_id:
            return redirect("topic_applications")

    if request.method == "POST":
        form = TopicApplicationDecisionForm(request.POST, instance=app)
        if form.is_valid():
            app = form.save(commit=False)
            app.decided_at = timezone.now()
            if app.status == TopicApplication.Status.APPROVED and not has_available_seat(app.topic.creator, app.student):
                messages.error(request, "Нет свободных мест по курсу студента для этого преподавателя.")
                return redirect("topic_applications")
            app.save()
            st = app.student
            if app.status == TopicApplication.Status.APPROVED:
                tchr = app.topic.creator
                work, _ = Work.objects.get_or_create(
                    author=st,
                    defaults={
                        "name": app.topic.title,
                        "description": app.topic.description,
                        "scientific_director": tchr,
                        "type_of_work": app.topic.get_work_kind_display(),
                    },
                )
                work.name = app.topic.title
                work.description = app.topic.description
                work.scientific_director = tchr
                work.type_of_work = app.topic.get_work_kind_display()
                work.save()
                st.scientific_director = tchr
                st.save()
                sync_teacher_course_counts(tchr)
                buck = student_course_bucket(st)
                if buck:
                    reject_pending_when_no_seats(tchr, buck)
                reject_other_pending_applications_for_topic(app.topic, st.id)
                reject_other_pending_for_student(st, tchr.id)
                _ensure_work_document(work)
                _generate_initial_docx(work, uploaded_by=request.user)
            body = f"{app.get_status_display()}: {app.topic.title}"
            if app.status == TopicApplication.Status.REJECTED and (app.decision_comment or "").strip():
                body += f"\nКомментарий: {app.decision_comment.strip()}"
            if app.status == TopicApplication.Status.REJECTED:
                body += f"\nОт кого: {user_display_name(request.user)}"
            notify(st.user, "Решение по заявке на тему", body, "")
            return redirect("topic_applications")
    else:
        form = TopicApplicationDecisionForm(instance=app)
    return render(request, "works/topic_decide.html", {"form": form, "application": app})


@require_user_types("teacher", "department_admin")
def decide_topic_proposal(request, proposal_id: int):
    prop = get_object_or_404(StudentTopicProposal, id=proposal_id)
    if request.user.user_type == "teacher" and prop.teacher_id != request.user.teacher.id:
        return redirect("topic_applications")
    if request.user.user_type == "department_admin":
        dept_id = getattr(getattr(request.user, "teacher", None), "department_id", None)
        if dept_id and prop.teacher.department_id != dept_id:
            return redirect("topic_applications")

    if request.method == "POST":
        form = StudentTopicProposalDecisionForm(request.POST, instance=prop)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.decided_at = timezone.now()
            if prop.status == StudentTopicProposal.Status.APPROVED and not has_available_seat(prop.teacher, prop.student):
                messages.error(request, "Нет свободных мест по курсу студента для этого преподавателя.")
                return redirect("topic_applications")
            prop.save()
            st = prop.student
            if prop.status == StudentTopicProposal.Status.APPROVED:
                tchr = prop.teacher
                tw = type_of_work_label_for_student(st)
                work, _ = Work.objects.get_or_create(
                    author=st,
                    defaults={
                        "name": prop.title,
                        "description": prop.description,
                        "scientific_director": tchr,
                        "type_of_work": tw,
                    },
                )
                work.name = prop.title
                work.description = prop.description
                work.scientific_director = tchr
                work.type_of_work = tw
                work.save()
                st.scientific_director = tchr
                st.save()
                sync_teacher_course_counts(tchr)
                buck = student_course_bucket(st)
                if buck:
                    reject_pending_when_no_seats(tchr, buck)
                reject_other_pending_for_student(st, tchr.id)
                _ensure_work_document(work)
                _generate_initial_docx(work, uploaded_by=request.user)
            body = f"{prop.get_status_display()}: {prop.title}"
            if prop.status == StudentTopicProposal.Status.REJECTED and (prop.decision_comment or "").strip():
                body += f"\nКомментарий: {prop.decision_comment.strip()}"
            if prop.status == StudentTopicProposal.Status.REJECTED:
                body += f"\nОт кого: {user_display_name(request.user)}"
            notify(st.user, "Решение по предложенной теме", body, "")
            return redirect("topic_applications")
    else:
        form = StudentTopicProposalDecisionForm(instance=prop)
    return render(request, "works/proposal_decide.html", {"form": form, "proposal": prop})
