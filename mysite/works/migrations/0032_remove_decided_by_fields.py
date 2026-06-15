                                   

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("works", "0031_remove_individualplan_created_by"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="topicapplication",
            name="decided_by",
        ),
        migrations.RemoveField(
            model_name="studenttopicproposal",
            name="decided_by",
        ),
    ]

