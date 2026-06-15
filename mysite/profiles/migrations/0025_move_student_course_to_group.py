from __future__ import annotations

import django.core.validators
from django.db import migrations, models


def _copy_course_from_students_to_groups(apps, schema_editor):
    """
    Best-effort migration: if a group has no course set, but at least one student
    in that group has Student.course filled (legacy), copy it to Group.course.
    """
    Student = apps.get_model("users", "Student")
    Group = apps.get_model("users", "Group")

    for g in Group.objects.filter(course__isnull=True):
        st = Student.objects.filter(group_id=g.id, course__isnull=False).order_by("-id").first()
        if st and getattr(st, "course", None) is not None:
            g.course = st.course
            g.save(update_fields=["course"])


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0024_remove_users_message"),
    ]

    operations = [
        migrations.AddField(
            model_name="group",
            name="course",
            field=models.PositiveSmallIntegerField(
                null=True,
                blank=True,
                verbose_name="Курс",
                help_text="Курс для группы. Бакалавриат: 3 или 4; магистратура: 1 или 2.",
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(8),
                ],
                db_index=True,
            ),
        ),
        migrations.RunPython(_copy_course_from_students_to_groups, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="student",
            name="course",
        ),
    ]

