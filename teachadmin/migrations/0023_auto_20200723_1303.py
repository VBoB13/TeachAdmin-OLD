# Generated by Django 3.0.6 on 2020-07-23 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teachadmin', '0022_student_subject'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='homeroom',
            options={'ordering': ['school', 'name']},
        ),
    ]
