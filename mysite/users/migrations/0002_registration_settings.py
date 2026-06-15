from django.db import migrations, models


def seed_registration_code(apps, schema_editor):
    RegistrationSettings = apps.get_model("accounts", "RegistrationSettings")
    if not RegistrationSettings.objects.exists():
        RegistrationSettings.objects.create(
            code="kubsu-student",
        )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RegistrationSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(help_text="Студенты вводят этот код на странице регистрации. Смените код, чтобы отозвать старые «приглашения».", max_length=256, verbose_name="Код приглашения")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Изменено")),
            ],
            options={
                "verbose_name": "Код регистрации студентов",
                "verbose_name_plural": "Код регистрации студентов",
            },
        ),
        migrations.RunPython(seed_registration_code, noop_reverse),
    ]
