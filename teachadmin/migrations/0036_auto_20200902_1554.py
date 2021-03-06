# Generated by Django 3.0.6 on 2020-09-02 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachadmin', '0035_auto_20200831_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeroom',
            name='grade',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homeroom',
            name='name',
            field=models.CharField(help_text='Anything within 50 characters.', max_length=50),
        ),
        migrations.AlterField(
            model_name='school',
            name='address',
            field=models.CharField(blank=True, help_text='English, please...', max_length=200),
        ),
        migrations.AlterField(
            model_name='school',
            name='name',
            field=models.CharField(help_text='Up to 256 characters', max_length=256),
        ),
    ]
