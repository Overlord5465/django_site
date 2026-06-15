from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("works", "0033_simplify_docx_metadata"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="work",
            name="status",
        ),
    ]

