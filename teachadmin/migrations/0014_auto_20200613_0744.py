# Generated by Django 3.0.6 on 2020-06-12 23:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teachadmin', '0013_auto_20200612_1238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='assignment_scores',
        ),
        migrations.RemoveField(
            model_name='student',
            name='test_scores',
        ),
        migrations.AddField(
            model_name='assignment',
            name='deadline',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='assignmentscore',
            name='student',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='teachadmin.Student'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentclasstestscore',
            name='student',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='teachadmin.Student'),
            preserve_default=False,
        ),
    ]
