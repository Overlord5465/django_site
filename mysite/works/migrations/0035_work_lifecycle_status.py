from django.db import migrations, models


def forwards_status_from_is_completed(apps, schema_editor):
    Work = apps.get_model("works", "Work")
    Work.objects.filter(is_completed=True).update(status="defended")
    Work.objects.filter(is_completed=False).update(status="not_ready")


class Migration(migrations.Migration):
    dependencies = [
        ("works", "0034_remove_work_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="work",
            name="status",
            field=models.CharField(
                choices=[
                    ("not_ready", "Работа не готова"),
                    ("ready", "Работа готова (ожидает нормоконтроль)"),
                    ("norm_ok", "Нормоконтроль пройден"),
                    ("defended", "Работа защищена (архив)"),
                ],
                db_index=True,
                default="not_ready",
                max_length=16,
                verbose_name="Статус",
            ),
        ),
        migrations.RunPython(forwards_status_from_is_completed, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="work",
            name="is_completed",
        ),
    ]
