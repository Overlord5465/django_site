from django.contrib import admin
from .models import Student, Teacher, Message, Group, DirectionOfStudy, InformationAboutTheNumberOfSeats


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'show_name', 'group']

    @admin.display(description='ФИО')
    def show_name(self, student: Student):
        return student.user.first_name


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'show_name', 'department']

    @admin.display(description='ФИО')
    def show_name(self, teacher: Teacher):
        return teacher.user.first_name


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['work', 'text', 'sender', 'recipient']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['group_number', 'direction_of_study']


@admin.register(DirectionOfStudy)
class DirectionOfStudyAdmin(admin.ModelAdmin):
    list_display = ['name_of_direction', 'direction_code', 'level_of_training']


@admin.register(InformationAboutTheNumberOfSeats)
class InformationAboutTheNumberOfSeatsAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'direction_of_study', 'current_amount', 'max_amount']

