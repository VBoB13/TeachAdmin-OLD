# Generated by Django 3.0.6 on 2020-07-15 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachadmin', '0021_auto_20200715_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='subject',
            field=models.ManyToManyField(to='teachadmin.Subject'),
        ),
    ]
