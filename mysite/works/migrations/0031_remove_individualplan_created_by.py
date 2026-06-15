                                   

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("works", "0030_remove_workdocument_workcomment"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="individualplan",
            name="created_by",
        ),
    ]

