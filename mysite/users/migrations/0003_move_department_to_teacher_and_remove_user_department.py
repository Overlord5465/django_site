from django.db import migrations


def move_department_to_teacher(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    Teacher = apps.get_model("users", "Teacher")

                                                                                                    
                                                                                
    for u in User.objects.exclude(department="").iterator():
        ut = getattr(u, "user_type", None) or ""
        if ut not in ("teacher", "department_admin"):
            continue
        t, _created = Teacher.objects.get_or_create(user_id=u.id)
        if not getattr(t, "department", ""):
            t.department = u.department
            t.save(update_fields=["department"])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_registration_settings"),
                                                                                                               
                                                                               
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(move_department_to_teacher, noop_reverse),
        migrations.RemoveField(model_name="user", name="department"),
    ]

