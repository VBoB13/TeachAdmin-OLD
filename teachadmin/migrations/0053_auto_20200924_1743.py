# Generated by Django 3.0.6 on 2020-09-24 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachadmin', '0052_auto_20200923_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('O', 'Other')], default='F', max_length=1),
        ),
    ]
