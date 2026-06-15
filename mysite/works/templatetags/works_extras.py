from django import template

from profiles.course_utils import format_student_course_line as _fmt_course
from profiles.fio_utils import format_user_fio

register = template.Library()


@register.filter
def user_fio(user):
    """Полное ФИО: фамилия + имя с отчеством (см. profiles.fio_utils)."""
    return format_user_fio(user)


@register.filter
def student_course_line(student):
    return _fmt_course(student)


@register.filter
def get_item(mapping, key):
    if mapping is None:
        return None
    try:
        return mapping.get(key)
    except AttributeError:
        return None


@register.filter
def getlist(querydict, key):
    if querydict is None or not hasattr(querydict, "getlist"):
        return []
    return querydict.getlist(key)
