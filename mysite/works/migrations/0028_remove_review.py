                                      

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("works", "0027_single_workversion_per_work"),
    ]

    operations = [
        migrations.DeleteModel(name="Review"),
    ]

