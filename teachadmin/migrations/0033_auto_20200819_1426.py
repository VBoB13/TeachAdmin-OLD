# Generated by Django 3.0.6 on 2020-08-19 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teachadmin', '0032_auto_20200816_1621'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['first_name']},
        ),
    ]
