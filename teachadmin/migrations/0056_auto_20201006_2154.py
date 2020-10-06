# Generated by Django 3.0.6 on 2020-10-06 13:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachadmin', '0055_auto_20201002_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeworkscore',
            name='turn_in_date',
            field=models.DateTimeField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='start_date',
            field=models.DateField(default=datetime.date(2020, 10, 6), null=True, verbose_name='Start date'),
        ),
        migrations.AlterField(
            model_name='lessontest',
            name='test_date',
            field=models.DateField(blank=True, default=datetime.date(2020, 10, 6), help_text='Format: yyyy-mm-dd'),
        ),
    ]