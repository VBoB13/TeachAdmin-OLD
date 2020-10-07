# Generated by Django 3.0.6 on 2020-10-07 06:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('teachadmin', '0060_auto_20201007_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='deadline',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Format: YYYY-MM-DD HH:MM:SS'),
        ),
        migrations.AlterField(
            model_name='assignmentscore',
            name='turn_in_time',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Format: YYYY-MM-DD HH:MM:SS'),
        ),
    ]