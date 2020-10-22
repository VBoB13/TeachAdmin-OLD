# Generated by Django 3.0.6 on 2020-10-22 10:44

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('teachadmin', '0064_auto_20201018_1716'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lessontestscore',
            options={'ordering': ['lessonTest', 'student', '-score']},
        ),
        migrations.AlterField(
            model_name='lessontest',
            name='test_date',
            field=models.DateField(blank=True, default=datetime.date(2020, 10, 22), help_text='Format: yyyy-mm-dd'),
        ),
        migrations.AlterField(
            model_name='student',
            name='homeroom',
            field=models.ForeignKey(blank=True, help_text='Optional.', null=True, on_delete=django.db.models.deletion.CASCADE, to='teachadmin.HomeRoom'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='country',
            field=django_countries.fields.CountryField(blank=True, help_text='Optional.', max_length=2),
        ),
    ]
