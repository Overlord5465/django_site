from django.contrib import admin

from users.department_admin_access import DepartmentAdminFullAccessMixin

from .models import Message


@admin.register(Message)
class MessageAdmin(DepartmentAdminFullAccessMixin, admin.ModelAdmin):
    list_display = ("sender", "recipient", "content", "timestamp", "read")
    list_filter = ("sender", "recipient", "read")
    search_fields = ("content", "sender__username", "recipient__username")
