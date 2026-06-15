from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest


def is_department_admin_user(user) -> bool:
    return bool(
        user
        and user.is_authenticated
        and user.is_staff
        and getattr(user, "user_type", None) == "department_admin"
    )


class DepartmentAdminFullAccessMixin:
    """
    Для пользователя с is_staff и user_type=department_admin — те же права на модель,
    что у суперпользователя (просмотр / добавление / изменение / удаление в админке).
    """

    def _dept_admin_full_access(self, request: HttpRequest) -> bool:
        u = request.user
        return bool(u.is_superuser or is_department_admin_user(u))

    def has_module_permission(self, request: HttpRequest) -> bool:
        if self._dept_admin_full_access(request):
            return True
        return super().has_module_permission(request)

    def has_view_permission(self, request: HttpRequest, obj=None) -> bool:
        if self._dept_admin_full_access(request):
            return True
        return super().has_view_permission(request, obj)

    def has_add_permission(self, request: HttpRequest) -> bool:
        if self._dept_admin_full_access(request):
            return True
        return super().has_add_permission(request)

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        if self._dept_admin_full_access(request):
            return True
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        if self._dept_admin_full_access(request):
            return True
        return super().has_delete_permission(request, obj)
