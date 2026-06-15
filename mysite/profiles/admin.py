from django.contrib import admin

from users.department_admin_access import DepartmentAdminFullAccessMixin

from .models import Department, DirectionOfStudy, Group, Student, Teacher, TeacherCourseSeat


@admin.register(Student)
class StudentAdmin(DepartmentAdminFullAccessMixin, admin.ModelAdmin):
    list_display = ["user", "show_name", "group"]

    @admin.display(description="ФИО")
    def show_name(self, student: Student):
        return student.user.first_name


@admin.register(Teacher)
class TeacherAdmin(DepartmentAdminFullAccessMixin, admin.ModelAdmin):
    list_display = ["user", "show_name", "department"]

    @admin.display(description="ФИО")
    def show_name(self, teacher: Teacher):
        return teacher.user.first_name


@admin.register(Group)
class GroupAdmin(DepartmentAdminFullAccessMixin, admin.ModelAdmin):
    list_display = ["group_number", "direction_of_study", "course"]


@admin.register(Department)
class DepartmentAdmin(DepartmentAdminFullAccessMixin, admin.ModelAdmin):
    list_display = ["name", "code"]
    search_fields = ["name", "code"]


@admin.register(DirectionOfStudy)
class DirectionOfStudyAdmin(DepartmentAdminFullAccessMixin, admin.ModelAdmin):
    list_display = ["name_of_direction", "direction_code", "level_of_training"]


@admin.register(TeacherCourseSeat)
class TeacherCourseSeatAdmin(DepartmentAdminFullAccessMixin, admin.ModelAdmin):
    list_display = ["teacher", "bucket", "current_amount", "max_amount"]
