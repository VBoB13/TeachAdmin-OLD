# Generated by Django 3.0.6 on 2020-06-08 02:23

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('teachadmin', '0003_auto_20200525_1031'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentClassTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('max_score', models.PositiveSmallIntegerField(default=100)),
                ('min_score', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.DeleteModel(
            name='Teacher',
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': [django.db.models.expressions.OrderBy(django.db.models.expressions.F('student_number'), nulls_last=True)]},
        ),
        migrations.AlterModelOptions(
            name='studentclass',
            options={'ordering': ['-grade']},
        ),
        migrations.RemoveField(
            model_name='student',
            name='behavior_score1',
        ),
        migrations.RemoveField(
            model_name='student',
            name='behavior_score2',
        ),
        migrations.RemoveField(
            model_name='student',
            name='behavior_score3',
        ),
        migrations.RemoveField(
            model_name='student',
            name='class_group',
        ),
        migrations.RemoveField(
            model_name='student',
            name='dwsquiz_score1',
        ),
        migrations.RemoveField(
            model_name='student',
            name='dwsquiz_score2',
        ),
        migrations.RemoveField(
            model_name='student',
            name='dwsquiz_score3',
        ),
        migrations.RemoveField(
            model_name='student',
            name='english_score1',
        ),
        migrations.RemoveField(
            model_name='student',
            name='english_score2',
        ),
        migrations.RemoveField(
            model_name='student',
            name='english_score3',
        ),
        migrations.RemoveField(
            model_name='student',
            name='listening_score1',
        ),
        migrations.RemoveField(
            model_name='student',
            name='listening_score2',
        ),
        migrations.RemoveField(
            model_name='student',
            name='listening_score3',
        ),
        migrations.RemoveField(
            model_name='student',
            name='phonics_score1',
        ),
        migrations.RemoveField(
            model_name='student',
            name='phonics_score2',
        ),
        migrations.RemoveField(
            model_name='student',
            name='phonics_score3',
        ),
        migrations.RemoveField(
            model_name='student',
            name='reading_score1',
        ),
        migrations.RemoveField(
            model_name='student',
            name='reading_score2',
        ),
        migrations.RemoveField(
            model_name='student',
            name='reading_score3',
        ),
        migrations.RemoveField(
            model_name='student',
            name='runningrecord_score1',
        ),
        migrations.RemoveField(
            model_name='student',
            name='runningrecord_score2',
        ),
        migrations.RemoveField(
            model_name='student',
            name='runningrecord_score3',
        ),
        migrations.AddField(
            model_name='student',
            name='studentClass',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='teachadmin.StudentClass'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_number',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='studentclass',
            name='grade',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='studentclasstest',
            name='studentClass',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='teachadmin.StudentClass'),
        ),
        migrations.AddField(
            model_name='student',
            name='tests',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='teachadmin.StudentClassTest'),
        ),
    ]
