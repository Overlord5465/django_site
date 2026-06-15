                                   

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0022_diploma_plan_v2"),
    ]

    operations = [
        migrations.DeleteModel(
            name="InformationAboutTheNumberOfSeats",
        ),
    ]

