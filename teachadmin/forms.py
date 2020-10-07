from django import forms
from django.contrib.auth.models import User
from .models import (Teacher, School, Student, 
                    Assignment, AssignmentScore,
                    HomeRoom, Subject, Exam, ExamScore,
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
        exclude = ['teacher',]


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['homeroom', 'subject', 'teacher']


class StudentToHomeRoomForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'gender']


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = '__all__'


class AssignmentScoreForm(forms.ModelForm):
    class Meta:
        model = AssignmentScore
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        assignment = kwargs.pop('assignment', None)
        subject = assignment.subject
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = subject.student_set.all()
        self.fields['assignment'].queryset = Assignment.objects.filter(pk=assignment.pk)
        self.fields['assignment'].empty_label = None


class HomeRoomForm(forms.ModelForm):
    class Meta:
        model = HomeRoom
        exclude = ('teacher', 'created_by')


class HomeRoomAddSubjectForm(forms.ModelForm):
    class Meta:
        model = HomeRoom
        fields = ('name',)


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = '__all__'


class HomeworkScoreForm(forms.ModelForm):
    class Meta:
        model = HomeworkScore
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        subject = kwargs.pop('subject', None)
        homework = kwargs.pop('homework', None)
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = subject.student_set.all()
        self.fields['homework'].queryset = Homework.objects.filter(pk=homework.pk)
        self.fields['homework'].empty_label = None


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
        exclude = ['subject',]


class ExamScoreForm(forms.ModelForm):
    class Meta:
        model = ExamScore
        fields = ['score', 'student']

    def __init__(self, *args, **kwargs):
        subject = kwargs.pop('subject', None)
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = subject.student_set.all()


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('name', 'subject')


class LessonTestForm(forms.ModelForm):
    class Meta:
        model = LessonTest
        fields = '__all__'


class LessonTestScoreForm(forms.ModelForm):
    class Meta:
        model = LessonTestScore
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        subject = kwargs.pop('subject', None)
        lessontest = kwargs.pop('lessontest', None)
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = subject.student_set.all()
        self.fields['lessonTest'].queryset = LessonTest.objects.filter(pk=lessontest.pk)
        self.fields['lessonTest'].empty_label = None


class BehaviorTypeForm(forms.ModelForm):
    class Meta:
        model = BehaviorType
        fields = ['name', 'description']


class BehaviorEventForm(forms.ModelForm):
    class Meta:
        model = BehaviorEvent
        fields = ['behaviorType', 'timestamp', 'comment']
