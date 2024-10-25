# Generated by Django 4.2.1 on 2024-10-20 21:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_teacher_current_amount_3_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='current_amount_4_course',
            field=models.IntegerField(blank=True, default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='current_amount_m',
            field=models.IntegerField(blank=True, default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='max_amount_3_course',
            field=models.IntegerField(blank=True, default=5, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='max_amount_4_course',
            field=models.IntegerField(blank=True, default=5, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='max_amount_m',
            field=models.IntegerField(blank=True, default=5, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)]),
        ),
    ]