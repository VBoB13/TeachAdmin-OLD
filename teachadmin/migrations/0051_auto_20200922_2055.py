# Generated by Django 3.0.6 on 2020-09-22 12:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('teachadmin', '0050_auto_20200922_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='deadline',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Format: YYYY-MM-DD HH:MM:SS'),
        ),
        migrations.AlterField(
            model_name='homework',
            name='max_score',
            field=models.PositiveSmallIntegerField(default=100, help_text='Default: 100'),
        ),
        migrations.AlterField(
            model_name='homework',
            name='min_score',
            field=models.PositiveSmallIntegerField(default=0, help_text='Default: 0'),
        ),
        migrations.AlterField(
            model_name='homework',
            name='name',
            field=models.CharField(help_text='Within 50 characters.', max_length=50),
        ),
    ]
