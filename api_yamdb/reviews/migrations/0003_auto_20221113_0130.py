# Generated by Django 2.2.16 on 2022-11-12 19:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20221109_2245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='rating',
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='Рейтинг ниже допустимого'), django.core.validators.MaxValueValidator(10, message='Рейтинг выше допустимого')]),
        ),
    ]
