"""Корзины курса для лимитов преподавателей и отображения."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from profiles.models import Student


class CourseBucket:
    B3 = "b3"
    B4 = "b4"
    M1 = "m1"
    M2 = "m2"
    CHOICES = (
        (B3, "Бакалавриат, 3 курс"),
        (B4, "Бакалавриат, 4 курс"),
        (M1, "Магистратура, 1 курс"),
        (M2, "Магистратура, 2 курс"),
    )
    ALL = (B3, B4, M1, M2)


def course_number_for_bucket(bucket: str) -> int:
    return {"b3": 3, "b4": 4, "m1": 1, "m2": 2}[bucket]


def bucket_for_registration_choice(value: str) -> str:
    """Значение из формы регистрации -> CourseBucket."""
    return {
        "bachelor_3": CourseBucket.B3,
        "bachelor_4": CourseBucket.B4,
        "master_1": CourseBucket.M1,
        "master_2": CourseBucket.M2,
    }[value]


def student_course_bucket(student) -> str | None:
    """Определяет корзину лимита для студента."""
    from profiles.models import DirectionOfStudy

    if not student:
        return None
    g = student.group
    c = getattr(g, "course", None) if g else None
    if c is None:
        return None
    if g and g.direction_of_study_id:
        lv = g.direction_of_study.level_of_training
        if lv == DirectionOfStudy.BACHELORS_DEGREE:
            if c == 3:
                return CourseBucket.B3
            if c == 4:
                return CourseBucket.B4
        if lv == DirectionOfStudy.MASTERS_DEGREE:
            if c == 1:
                return CourseBucket.M1
            if c == 2:
                return CourseBucket.M2
    if c == 3:
        return CourseBucket.B3
    if c == 4:
        return CourseBucket.B4
    if c == 1:
        return CourseBucket.M1
    if c == 2:
        return CourseBucket.M2
    return None


def format_student_course_line(student) -> str:
    """Строка для профиля: «Бакалавриат 3 курс», «Магистратура 1 курс», «Выпускник» и т.д."""
    from profiles.models import DirectionOfStudy

    if not student:
        return "Выпускник"

    g = student.group
    c = getattr(g, "course", None) if g else None

    def _from_course_number_no_direction() -> str | None:
        """Если направления нет — ориентируемся только на номер курса."""
        if c is None:
            return None
        if c == 3:
            return "Бакалавриат 3 курс"
        if c == 4:
            return "Бакалавриат 4 курс"
        if c == 1:
            return "Магистратура 1 курс"
        if c == 2:
            return "Магистратура 2 курс"
        return None

    if g and g.direction_of_study_id:
        lv = g.direction_of_study.level_of_training
        if lv == DirectionOfStudy.BACHELORS_DEGREE:
            if c == 3:
                return "Бакалавриат 3 курс"
            if c == 4:
                return "Бакалавриат 4 курс"
            if c is not None and c > 4:
                return "Выпускник"
            return "Выпускник"
        if lv == DirectionOfStudy.MASTERS_DEGREE:
            if c == 1:
                return "Магистратура 1 курс"
            if c == 2:
                return "Магистратура 2 курс"
            if c is not None and c > 2:
                return "Выпускник"
            return "Выпускник"

    if c is None:
        return "Выпускник"
    fallback = _from_course_number_no_direction()
    if fallback:
        return fallback
    return "Выпускник"
