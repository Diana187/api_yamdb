# Generated by Django 2.2.16 on 2022-11-06 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(max_length=255, null=True, verbose_name='код подтверждения'),
        ),
    ]