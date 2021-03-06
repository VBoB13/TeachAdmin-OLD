# Generated by Django 3.0.6 on 2020-09-21 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachadmin', '0048_auto_20200920_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='max_score',
            field=models.PositiveSmallIntegerField(default=100, help_text='Default: 100'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='min_score',
            field=models.PositiveSmallIntegerField(default=0, help_text='Default: 0'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='name',
            field=models.CharField(help_text='Anything within 100 characters.', max_length=100),
        ),
    ]
