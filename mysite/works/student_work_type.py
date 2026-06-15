from __future__ import annotations

from profiles.course_utils import CourseBucket, student_course_bucket
from profiles.models import DirectionOfStudy

from works.models import Topic


def type_of_work_label_for_student(student) -> str:
    """Подпись типа работы по курсу и уровню подготовки (без привязки к теме из банка)."""
    if not student:
        return ""
    bucket = student_course_bucket(student)
    if bucket == CourseBucket.B3:
        return str(Topic.WorkKind.COURSEWORK.label)
    if bucket == CourseBucket.B4:
        return str(Topic.WorkKind.BACHELOR.label)
    if bucket in (CourseBucket.M1, CourseBucket.M2):
        return str(Topic.WorkKind.MASTER.label)

    g = getattr(student, "group", None)
    c = getattr(g, "course", None) if g else None
    if g and getattr(g, "direction_of_study_id", None):
        lv = g.direction_of_study.level_of_training
        if lv == DirectionOfStudy.BACHELORS_DEGREE:
            if c == 3:
                return str(Topic.WorkKind.COURSEWORK.label)
            if c == 4:
                return str(Topic.WorkKind.BACHELOR.label)
        if lv == DirectionOfStudy.MASTERS_DEGREE:
            return str(Topic.WorkKind.MASTER.label)

    if c == 3:
        return str(Topic.WorkKind.COURSEWORK.label)
    if c == 4:
        return str(Topic.WorkKind.BACHELOR.label)
    if c in (1, 2):
        return str(Topic.WorkKind.MASTER.label)
    return "Работа"
