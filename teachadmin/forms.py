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

    def __init__(self, *args, **kwargs):
        subject = kwargs.pop('subject', None)
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.filter(pk=subject.pk)
        self.fields['subject'].empty_label = None
        self.initial['creator'] = teacher


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

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', False)
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields['school'].queryset = teacher.school_set.all()
            self.fields['school'].empty_label = None


class HomeRoomAddSubjectForm(forms.ModelForm):
    class Meta:
        model = HomeRoom
        fields = ('name',)
    
    subjects = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        homeroom = kwargs.pop('homeroom', None)
        super().__init__(*args, **kwargs)
        if teacher and homeroom:
            self.fields['subjects'].queryset = teacher.subject_set.all()
            self.fields['subjects'].initial = [s.pk for s in homeroom.subject_set.all()]
            self.fields['subjects'].empty_label = None
            self.fields['subjects'].help_text = "Ctrl + Left-Click for selecting and de-selecting Subjects."


class HomeRoomAddStudentForm(forms.ModelForm):
    class Meta:
        model = HomeRoom
        fields = ('name',)

    students = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        homeroom = kwargs.pop('homeroom', None)
        super().__init__(*args, **kwargs)
        if teacher and homeroom:
            self.fields['students'].queryset = teacher.student_set.exclude(homeroom=homeroom)
            self.fields['students'].empty_label = None
            self.fields['students'].help_text = "Ctrl + Left-Click to select and de-select students."


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

    students = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        subject = kwargs.pop('subject', None)
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        if teacher and subject:
            self.fields['students'].queryset = teacher.student_set.all()
            self.fields['students'].initial = [s.pk for s in subject.student_set.all()]
        self.fields['students'].empty_label = None


class SubjectToStudentForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        subject_pk = kwargs.pop('subject_pk', None)
        super().__init__(*args, **kwargs)
        if subject_pk:
            self.fields['subject'].queryset = Subject.objects.filter(pk=subject_pk)
        self.fields['subject'].empty_label = None


class ExamScoreForm(forms.ModelForm):
    class Meta:
        model = ExamScore
        fields = ['score', 'student']

    def __init__(self, *args, **kwargs):
        subject = kwargs.pop('subject', None)
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = subject.student_set.all()
        self.fields['student'].empty_label = None


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        exclude = ('subject',)


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
