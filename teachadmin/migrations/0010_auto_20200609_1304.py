# Generated by Django 3.0.6 on 2020-06-09 05:04

from django.db import migrations
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('teachadmin', '0009_auto_20200609_1241'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': [django.db.models.expressions.OrderBy(django.db.models.expressions.F('student_number'), nulls_last=True)]},
        ),
    ]
