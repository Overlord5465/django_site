from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from users.department_admin_access import DepartmentAdminFullAccessMixin

from .models import RegistrationSettings


@admin.register(RegistrationSettings)
class RegistrationSettingsAdmin(DepartmentAdminFullAccessMixin, admin.ModelAdmin):
    list_display = ("code_short", "updated_at")
    readonly_fields = ("updated_at",)

    @admin.display(description="Код (фрагмент)")
    def code_short(self, obj):
        if not obj or not obj.pk:
            return "—"
        c = (obj.code or "").strip()
        if not c:
            return "—"
        if len(c) <= 16:
            return c
        return c[:14] + "…"

    def has_add_permission(self, request):
        if RegistrationSettings.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(get_user_model())
class CustomUserAdmin(DepartmentAdminFullAccessMixin, UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("RBAC", {"fields": ("user_type",)}),
    )
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "user_type",
        "is_staff",
        "is_active",
    )
    list_filter = ("user_type", "is_staff", "is_active")
