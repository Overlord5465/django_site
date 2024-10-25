# Generated by Django 4.2.1 on 2024-10-19 07:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('works', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(db_index=True, max_length=100, verbose_name='Категория')),
                ('recipient', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages3', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages2', to=settings.AUTH_USER_MODEL)),
                ('work', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages1', to='works.work')),
            ],
        ),
    ]
