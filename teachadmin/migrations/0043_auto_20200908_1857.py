# Generated by Django 3.0.6 on 2020-09-08 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachadmin', '0042_auto_20200907_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='end_date',
            field=models.DateTimeField(null=True, verbose_name='End date'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='start_date',
            field=models.DateTimeField(null=True, verbose_name='Start date'),
        ),
    ]
