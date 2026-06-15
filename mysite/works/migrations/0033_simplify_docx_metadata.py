                                   

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("works", "0032_remove_decided_by_fields"),
    ]

    operations = [
        migrations.RenameField(
            model_name="work",
            old_name="docx_uploaded_at",
            new_name="docx_updated_at",
        ),
        migrations.RemoveField(
            model_name="work",
            name="docx_uploaded_by",
        ),
        migrations.RemoveField(
            model_name="work",
            name="docx_comment",
        ),
        migrations.RemoveField(
            model_name="work",
            name="docx_is_final",
        ),
    ]

