from __future__ import annotations

from profiles.course_utils import CourseBucket, student_course_bucket
from profiles.models import Student, Teacher, TeacherCourseSeat


def ensure_teacher_seats(teacher: Teacher) -> None:
    for b in CourseBucket.ALL:
        TeacherCourseSeat.objects.get_or_create(
            teacher=teacher,
            bucket=b,
            defaults={"current_amount": 0, "max_amount": 5},
        )


def sync_teacher_course_counts(teacher: Teacher) -> None:
    ensure_teacher_seats(teacher)
    counts = {b: 0 for b in CourseBucket.ALL}
    for st in Student.objects.filter(scientific_director=teacher).select_related("group__direction_of_study"):
        buck = student_course_bucket(st)
        if buck:
            counts[buck] = counts.get(buck, 0) + 1
    for b, n in counts.items():
        TeacherCourseSeat.objects.filter(teacher=teacher, bucket=b).update(current_amount=n)
