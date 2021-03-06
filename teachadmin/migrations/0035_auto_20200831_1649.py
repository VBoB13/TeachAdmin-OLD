# Generated by Django 3.0.6 on 2020-08-31 08:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('teachadmin', '0034_auto_20200819_1903'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='examscore',
            options={'ordering': ['exam', 'timestamp', 'score', 'student']},
        ),
        migrations.AddField(
            model_name='homeroom',
            name='created_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
