# Generated by Django 3.0.6 on 2020-09-02 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachadmin', '0036_auto_20200902_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeroom',
            name='grade',
            field=models.PositiveSmallIntegerField(blank=True, help_text='Positive numbers, please.', null=True),
        ),
    ]
