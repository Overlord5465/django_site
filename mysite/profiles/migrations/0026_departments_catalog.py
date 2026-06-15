from __future__ import annotations

from django.db import migrations, models


def seed_departments_and_migrate_teachers(apps, schema_editor):
    Department = apps.get_model("users", "Department")
    Teacher = apps.get_model("users", "Teacher")

                                                                                     
                                                                       
    legacy_map = {
        "IT": ("IT", "Кафедра информационных технологий"),
        "CT": ("CT", "Кафедра вычислительных технологий"),
        "MM": ("MM", "Кафедра математического моделирования"),
        "DAAAI": ("DAAAI", "Кафедра анализа данных и искусственного интеллекта"),
        "AM": ("AM", "Кафедра прикладной математики"),
    }

    dep_by_code = {}
    for code, (c, name) in legacy_map.items():
        dep, _ = Department.objects.get_or_create(code=c, defaults={"name": name})
        dep_by_code[code] = dep

    for t in Teacher.objects.all():
        legacy_code = getattr(t, "department", None)
        if legacy_code in dep_by_code:
            t.department_id = dep_by_code[legacy_code].id
            t.save(update_fields=["department"])


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0025_move_student_course_to_group"),
    ]

    operations = [
        migrations.CreateModel(
            name="Department",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(db_index=True, max_length=32, unique=True, verbose_name="Код")),
                ("name", models.CharField(db_index=True, max_length=200, unique=True, verbose_name="Название")),
            ],
            options={
                "verbose_name": "Кафедра",
                "verbose_name_plural": "Кафедры",
                "ordering": ("name",),
            },
        ),
        migrations.AddField(
            model_name="teacher",
            name="department_fk",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.SET_NULL,
                related_name="teachers",
                to="users.department",
                verbose_name="Кафедра",
            ),
        ),
        migrations.RunPython(seed_departments_and_migrate_teachers, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="teacher",
            name="department",
        ),
        migrations.RenameField(
            model_name="teacher",
            old_name="department_fk",
            new_name="department",
        ),
    ]

