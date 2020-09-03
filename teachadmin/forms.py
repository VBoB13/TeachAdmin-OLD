from django import forms
from django.contrib.auth.models import User
from .models import (Teacher, School, Student, StudentClass, 
                    StudentClassTest, Assignment, HomeRoom,
                    Subject, Exam, ExamScore,
                    Lesson, LessonTest, LessonTestScore,
                    BehaviorType, BehaviorEvent,
                    Homework, HomeworkScore)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['portfolio_site', 'profile_pic']


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ('name', 'address')


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'gender', 'homeroom',
                  'student_number', ]

class StudentToHomeRoomForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'gender']


class StudentClassForm(forms.ModelForm):
    class Meta:
        model = StudentClass
        fields = ['school', 'name', 'grade']


class StudentClassTestForm(forms.ModelForm):
    class Meta:
        model = StudentClassTest
        fields = ['name', 'min_score', 'max_score']


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['name', 'min_score', 'max_score', 'subject']


class StudentClassFormWithFile(forms.Form):
    file = forms.FileField()


class HomeRoomForm(forms.ModelForm):
    class Meta:
        model = HomeRoom
        fields = ('name', 'school', 'grade')


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = '__all__'


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']


class SubjectToStudentForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'date', 'min_score', 'max_score']


class ExamScoreForm(forms.ModelForm):
    class Meta:
        model = ExamScore
        fields = ['score']


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('name', 'subject')


class LessonTestForm(forms.ModelForm):
    class Meta:
        model = LessonTest
        fields = ('name', 'lesson', 'test_date', 'min_score', 'max_score')


class LessonTestScoreForm(forms.ModelForm):
    class Meta:
        model = LessonTestScore
        fields = ('score', 'lessonTest')


class BehaviorTypeForm(forms.ModelForm):
    class Meta:
        model = BehaviorType
        fields = ['name', 'description']


class BehaviorEventForm(forms.ModelForm):
    class Meta:
        model = BehaviorEvent
        fields = ['behaviorType', 'timestamp', 'comment']
