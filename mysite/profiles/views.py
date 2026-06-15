from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from mysite import settings
from .forms import (LoginUserForm, RegisterUserForm, ProfileUserForm,
    UserPasswordChangeForm, UserForm, StudentForm, DepartmentAdminProfileForm)
from .models import Teacher, Student, TeacherCourseSeat
from profiles.course_utils import format_student_course_line
from profiles.seat_sync import sync_teacher_course_counts


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('profiles:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        student = Student.objects.get(user=self.object)
        student.group = form.cleaned_data["group"]
        student.save(update_fields=["group"])
        return response


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {
        'title': "Профиль пользователя",
    }

    def get_success_url(self):
        return reverse_lazy('profiles:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("profiles:password_change_done")
    template_name = "users/password_change_form.html"


def update_profile(request):
    user = request.user
    is_teacher = Teacher.objects.filter(user=user).exists()
    is_student = Student.objects.filter(user=user).exists()
    user_type = getattr(user, "user_type", None)

    profile = None
    profile_form = None
    user_form = None
    teacher_seats = None

    if is_teacher:
        profile = Teacher.objects.get(user=user)
    elif is_student:
        profile = Student.objects.get(user=user)
    elif user_type == "department_admin":
        profile = None
    else:
        profile = None

    if request.method == "POST":
        if is_teacher:
            user_form = UserForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
        elif is_student:
            user_form = UserForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
                profile.refresh_from_db()
        elif user_type == "department_admin":
            user_form = DepartmentAdminProfileForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
        else:
            user_form = UserForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
    else:
        if is_teacher:
            user_form = UserForm(instance=user)
            profile_form = None
        elif is_student:
            user_form = UserForm(instance=user)
            profile_form = None
        elif user_type == "department_admin":
            user_form = DepartmentAdminProfileForm(instance=user)
        else:
            user_form = UserForm(instance=user)

    student_course_line = None
    if is_teacher and profile is not None:
        teacher_seats = TeacherCourseSeat.objects.filter(teacher=profile).order_by("bucket")
    elif is_student and profile is not None:
        teacher_seats = None
        student_course_line = format_student_course_line(profile)
    else:
        teacher_seats = None

    return render(
        request,
        "users/edit_profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "teacher_seats": teacher_seats,
            "student_course_line": student_course_line,
            "student_group": (profile.group if is_student and profile is not None else None),
        },
    )
