                                   

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0023_remove_informationaboutthenumberofseats"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Message",
        ),
    ]

