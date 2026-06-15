                                      

from __future__ import annotations

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("works", "0029_work_docx_single_file"),
    ]

    operations = [
        migrations.DeleteModel(name="WorkComment"),
        migrations.DeleteModel(name="WorkDocument"),
    ]

