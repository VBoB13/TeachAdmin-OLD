# Generated by Django 3.0.6 on 2020-09-28 13:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('teachadmin', '0053_auto_20200924_1743'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='behaviorevent',
            options={'ordering': ['timestamp', 'behaviorType', 'student']},
        ),
        migrations.RemoveField(
            model_name='behaviorevent',
            name='creator',
        ),
        migrations.AddField(
            model_name='homeworkscore',
            name='turn_in_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='behaviorevent',
            name='comment',
            field=models.TextField(max_length=300),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_number',
            field=models.CharField(blank=True, default='', help_text='Within 20 characters.', max_length=20),
        ),
    ]