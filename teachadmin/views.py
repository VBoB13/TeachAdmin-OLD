from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.conf import settings

from .models import (Teacher, School, Student,
                        Assignment, AssignmentScore,
                        HomeRoom, Subject, Exam, ExamScore,
                        Lesson, LessonTest, LessonTestScore,
                        BehaviorType, BehaviorEvent, 
                        Homework, HomeworkScore)
from . import forms
from django import forms as djangoforms

from .graph import Graph

from datetime import datetime
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters

import os
import io
import urllib, base64

# Create your views here.

class AboutView(generic.TemplateView):
    template_name = 'teachadmin/about.html'


class AssignmentDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/assignment_detail.html'

    template_name = 'teachadmin/assignment_detail.html'
    context_object_name = 'assignment'

    def get_queryset(self):
        return Assignment.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        students = self.object.subject.student_set.all()
        assignmentscores = self.object.assignmentscore_set.filter(student__in=students)
        context['assignmentscores'] = assignmentscores

        graph = Graph(self.object)
        context['graph'] = graph.uri

        return context


class AssignmentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Assignment
    success_url = reverse_lazy('teachadmin:subject_list')


class AssignmentCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/index.html'
    
    model = Assignment
    form_class = forms.AssignmentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        view_title = "Add Assignment"

        if self.kwargs.get('subject_pk'):
            subject = get_object_or_404(Subject, pk=self.kwargs['subject_pk'])
            teacher = get_object_or_404(Teacher, user=self.request.user)
            form = forms.AssignmentForm(initial={"subject":subject, "teacher":teacher})
            context['form'] = form

            view_title += " to {}".format(subject)
            context['view_title'] = view_title


        return context

    def form_valid(self, form):
        assignment = form.save()
        teacher = get_object_or_404(Teacher, user=self.request.user)
        assignment.creator.add(teacher)
        return super().form_valid(form)


class AssignmentUpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/assignment_detail.html'

    form_class = forms.AssignmentForm
    model = Assignment
    context_object_name = 'assignment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_title = "Update {}".format(self.object)
        context["view_title"] = view_title
        return context


class AssignmentScoreCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = 'teachadmin/login.'
    redirect_field_name = 'teachadmin/assignmentscore_form.html'

    model = AssignmentScore
    form_class = forms.AssignmentScoreForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        
        assignment = get_object_or_404(
            Assignment, pk=self.kwargs.get('assignment_pk'))
        kwargs['assignment'] = assignment

        return kwargs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        assignment = get_object_or_404(Assignment, pk=self.kwargs.get('assignment_pk'))
        context['assignment'] = assignment

        view_title = "Add score to"
        context['view_title'] = view_title

        return context



class ExamListView(LoginRequiredMixin, generic.ListView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/index.html'

    template_name = 'teachadmin/exam_list.html'
    context_object_name = 'exams'

    def get_queryset(self):
        subject = get_object_or_404(Subject, pk=self.kwargs['subject_pk'])
        return Exam.objects.filter(subject=subject)


class ExamDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/index.html'

    template_name = 'teachadmin/exam_detail.html'
    context_object_name = 'exam'

    def get_queryset(self):
        return Exam.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        subject = get_object_or_404(Subject, pk=self.kwargs.get('subject_pk'))
        self.view_title = "{} ({})".format(self.object, subject)
        context['view_title'] = self.view_title

        graph = Graph(self.object)
        context['graph'] = graph.uri

        return context


class ExamCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/exam_detail.html'

    model = Exam
    form_class = forms.ExamForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        view_title = "Add exam"

        if self.kwargs.get('subject_pk'):
            subject = get_object_or_404(Subject, pk=self.kwargs['subject_pk'])
            context['subject'] = subject
            view_title += " to {}".format(subject)

        context['view_title'] = view_title

        return context


    def form_valid(self, form):
        subject = get_object_or_404(Subject, pk=self.kwargs['subject_pk'])
        form.instance.subject = subject
        form.save()
        return super().form_valid(form)


class ExamDeleteView(LoginRequiredMixin, generic.DeleteView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/subject_list.html'

    model = Exam
    success_url = reverse_lazy('teachadmin:subject_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        view_title = "Delete {}".format(self.object)
        context["view_title"] = view_title

        return context


class ExamUpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/exam_form.html'

    form_class = forms.ExamForm
    model = Exam
    context_object_name = 'exam'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_title"] = "Update {}".format(self.object)
        return context
    

class ExamScoreDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/index.html'

    template_name = 'teachadmin/examscore_detail.html'
    context_object_name = 'examscore'

    def get_queryset(self):
        return ExamScore.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        view_title = "Score details for "
        context['view_title'] = view_title

        return context


class ExamScoreCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/exam_detail.html'

    model = ExamScore
    form_class = forms.ExamScoreForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        subject = get_object_or_404(Subject, pk=self.kwargs.get('subject_pk'))
        kwargs['subject'] = subject
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        exam = get_object_or_404(Exam, pk=self.kwargs.get('exam_pk'))
        context['exam'] = exam
        
        subject = get_object_or_404(Subject, pk=self.kwargs.get('subject_pk'))
        context['subject'] = subject
        
        view_title = "Add score to {}".format(exam)
        context['view_title'] = view_title

        return context

    def form_valid(self, form):
        form.instance.student = get_object_or_404(Student, pk=self.request.POST.get('student'))
        form.instance.exam = get_object_or_404(Exam, pk=self.kwargs.get('exam_pk'))
        form.save()

        return super().form_valid(form)


class ExamScoreUpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/examscore_form.html'

    form_class = forms.ExamScoreForm
    model = ExamScore
    context_object_name = 'examscore'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_title = "Update {}".format(self.object)
        context["view_title"] = view_title
        return context
    

class ExamScoreDeleteView(LoginRequiredMixin, generic.DeleteView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/examscore_confirm_delete.html'

    model = ExamScore
    success_url = reverse_lazy('teachadmin:subject_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_title = "Delete {}".format(self.object)
        context["view_title"] = view_title
        return context
    

class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/index.html'

    template_name = 'teachadmin/index.html'
    context_object_name = 'teacher'

    def get_queryset(self):
        """Return a list of 'StudentClass'es sorted by name"""
        if self.request.user.username == 'admin':
            self.context_object_name = 'schools'
            return School.objects.all()
        else:
            teacher = get_object_or_404(Teacher, user=self.request.user)
            return teacher

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        teacher = get_object_or_404(Teacher, user=self.request.user)
        schools = teacher.school_set.all()
        homerooms = teacher.homeroom_set.all()
        subjects = teacher.subject_set.all()
        all_students = teacher.student_set.all()
        other_students = all_students.exclude(homeroom__in=homerooms, subject__in=subjects)

        context['teacher'] = teacher
        context['schools'] = schools
        context['homerooms'] = homerooms
        context['subjects'] = subjects
        context['all_students'] = all_students
        context['other_students'] = other_students

        return context


class HomeRoomListView(LoginRequiredMixin, generic.ListView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/school_list.html'

    template_name = 'teachadmin/homeroom_list.html'
    context_object_name = 'homerooms'

    def get_queryset(self):
        teacher = get_object_or_404(Teacher, user=self.request.user)
        return teacher.homeroom_set.all()


class HomeRoomDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/homeroom_detail.html'

    model = HomeRoom
    template_name = 'teachadmin/homeroom_detail.html'
    context_object_name = 'homeroom'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teacher'] = get_object_or_404(Teacher, user=self.request.user)
        context['subject'] = True

        graph = Graph(self.object)
        context['graph'] = graph.uri

        return context
    

class HomeRoomCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/homeroom_detail.html'
    
    model = HomeRoom
    form_class = forms.HomeRoomForm

    def _process_homeroomfile(self, homeroom):
        if self.request.method == "POST":
            try:
                results = pd.read_csv(
                    self.request.FILES['homeroomfile'])
            except Exception as err:
                print("Unable to read .csv-file")
                print(err)
                raise Http404("Unable to read CSV-file")
            else:
                print(results)
                results.info()

                for row in results.itertuples():
                    student, created = Student.objects.get_or_create(
                        student_number=row.Number,
                        first_name=row.First,
                        last_name=row.Last,
                        gender=row.Gender,
                        homeroom=homeroom
                    )
                    print(student)
        else:
            print("Try with a POST-reqest next time.")


    def form_valid(self, form):
        teacher = get_object_or_404(Teacher, user=self.request.user)

        homeroom = form.save()
        teacher.homeroom_set.add(homeroom)

        if self.request.FILES.get('homeroomfile', False):
            self._process_homeroomfile(homeroom)

        return HttpResponseRedirect(homeroom.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.kwargs.get('school_pk'):
            school = get_object_or_404(School, pk=self.kwargs['school_pk'])
            form = forms.HomeRoomForm(initial={'school':school})
            context['form'] = form
            self.view_title = 'Create Homeroom for {}'.format(school)
        else:
            self.view_title = 'Create Homeroom'
    
        context['view_title'] = self.view_title

        return context


class HomeRoomUpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/homeroom_detail.html'

    form_class = forms.HomeRoomForm
    model = HomeRoom
    context_object_name = 'homeroom'

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('subject'):
            self.form_class = forms.HomeRoomAddSubjectForm
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        homeroom = form.save()
        if self.form_class == forms.HomeRoomAddSubjectForm:
            for subject in Subject.objects.filter(pk__in=self.request.POST.getlist('selected_subjects')):
                homeroom.subject_set.add(subject)
                if homeroom.has_students():
                    for student in homeroom.student_set.all():
                        subject.student_set.add(student)
        else:
            students = Student.objects.filter(pk__in=self.request.POST.getlist('selected_students'))
            if students.count() >= 1:
                for student in students:
                    if student.homeroom == None:
                        student.homeroom = homeroom
                        student.save()
                    else:
                        print("Student ({}) already has a homeroom.".format(student))

        return super().form_valid(form)
    
    def get_context_data(self):
        context = super().get_context_data()
        
        self.view_title = 'Update Homeroom'
        context['view_title'] = self.view_title

        teacher = get_object_or_404(Teacher, user=self.request.user)
        context['teacher'] = teacher
        if self.form_class == forms.HomeRoomAddSubjectForm:
            context['subject'] = self.kwargs.get('subject')
            
        
        available_students = Student.objects.filter(teacher=teacher)
        context['available_students'] = available_students

        return context


class HomeRoomDeleteView(LoginRequiredMixin, generic.DeleteView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/homeroom_list.html'

    model = HomeRoom
    success_url = reverse_lazy('teachadmin:homeroom_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        view_title = "Delete {}".format(self.object)
        context['view_title'] = view_title

        return context


class HomeworkCreateView(LoginRequiredMixin, generic.CreateView):

    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/index.html'

    model = Homework
    form_class = forms.HomeworkForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        view_title = "Add homework"

        if self.kwargs.get('subject_pk') and self.kwargs.get('lesson_pk'):
            subject = get_object_or_404(Subject, pk=self.kwargs['subject_pk'])
            lesson = get_object_or_404(Lesson, pk=self.kwargs['lesson_pk'])
            
            view_title += " to {} ({})".format(lesson, subject)

            form = forms.HomeworkForm(initial={"lesson": lesson})
            context['form'] = form
        
        context['view_title'] = view_title

        return context


class HomeworkDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/homework_detail.html'

    template_name = redirect_field_name
    context_object_name = 'homework'
    model = Homework

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        view_title = "{} ({})".format(self.object, self.object.lesson)
        context['view_title'] = view_title

        graph = Graph(self.object)
        context['graph'] = graph.uri

        return context


class HomeworkUpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/homework_form.html'

    form_class = forms.HomeworkForm
    model = Homework
    context_object_name = 'homework'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_title = "Update {}".format(self.object)
        context["view_title"] = view_title
        return context
    

class HomeworkDeleteView(LoginRequiredMixin, generic.DeleteView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/homework_confirm_delete.html'

    model = Homework
    success_url = reverse_lazy('teachadmin:subject_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_title = "Delete {}".format(self.object)
        context["view_title"] = view_title
        return context
    

class HomeworkScoreCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/homeworkscore_form.html'

    model = HomeworkScore
    form_class = forms.HomeworkScoreForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        
        subject = get_object_or_404(Subject, pk=self.kwargs.get('subject_pk'))
        kwargs['subject'] = subject

        homework = get_object_or_404(Homework, pk=self.kwargs.get('homework_pk'))
        kwargs['homework'] = homework

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        view_title = 'Add homework score'
        subject = get_object_or_404(Subject, pk=self.kwargs.get('subject_pk'))
        
        context['subject'] = subject
        context['view_title'] = view_title

        return context
    
    def form_valid(self, form):

        student = get_object_or_404(Student, pk=self.request.POST.get('student'))
        form.instance.student = student

        return super().form_valid(form)


class LessonDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/lesson_detail.html'

    template_name = 'teachadmin/lesson_detail.html'
    context_object_name = 'lesson'
    model = Lesson

    def create_graph(self):
        """ Generates a graph for the view that gets saved onto the server
            and then loaded as a picture through <img>-tag in template 
            INPUT: None
            OUTPUT: Bool (True/False) """

        lessontests = self.object.lessontest_set.all().order_by('test_date')
        homeworks = self.object.homework_set.all()
        students = self.object.subject.student_set.all()

        lessontestscores = LessonTestScore.objects.filter(lessonTest__in=lessontests).order_by('student', 'lessonTest')
        homeworkscores = HomeworkScore.objects.filter(homework__in=homeworks).order_by('student', 'homework')

        index = []
        scores = {
            'Student':[],
        }
        testscores = {}
        homeworkscoredict = {}
        
        for count, student in enumerate(students):
            add_score = False
            for lessontestscore in lessontestscores.filter(student=student):
                if '{}({})'.format(lessontestscore.lessonTest, lessontestscore.lessonTest.pk) not in scores.keys():
                    scores['{}({})'.format(lessontestscore.lessonTest, lessontestscore.lessonTest.pk)] = []
                    testscores['{}({})'.format(lessontestscore.lessonTest, lessontestscore.lessonTest.pk)] = []
                testscores['{}({})'.format(
                    lessontestscore.lessonTest, lessontestscore.lessonTest.pk
                    )].append(round(((lessontestscore.score/lessontestscore.lessonTest.max_score)*100),1))
            
            for key in testscores.keys():
                scores[key].append(max(testscores[key]))
                add_score = True

            for homeworkscore in homeworkscores.filter(student=student):
                if '{}({})'.format(homeworkscore.homework, homeworkscore.homework.pk) not in scores.keys():
                    scores['{}({})'.format(homeworkscore.homework,
                                           homeworkscore.homework.pk)] = []
                    homeworkscoredict['{}({})'.format(
                        homeworkscore.homework, homeworkscore.homework.pk)] = []
                homeworkscoredict['{}({})'.format(
                    homeworkscore.homework, homeworkscore.homework.pk
                )].append(round(((homeworkscore.score/homeworkscore.homework.max_score)*100), 1))

            for key in homeworkscoredict.keys():
                scores[key].append(max(homeworkscoredict[key]))
                add_score = True

            if add_score:
                index.append(count)
                scores['Student'].append(str(student))

        print(scores)
        scoresDF = pd.DataFrame(data=scores, index=index)
        checkDF = scoresDF.iloc[:,1:]

        if checkDF.empty:
            return False

        fig = plt.figure()
        sns.set_style(style='darkgrid')
        plt.style.use("dark_background")
        sns.swarmplot(
            data=scoresDF,
            palette="bright"
        )
        axes = fig.gca()
        axes.set_ylim(
            (scoresDF.min(axis=0, numeric_only=True).min())-int(
                (scoresDF.max(axis=0, numeric_only=True).max() -
                scoresDF.min(axis=0, numeric_only=True).min())*0.1
            ),
            (scoresDF.max(axis=0, numeric_only=True).max())+int(
                (scoresDF.max(axis=0, numeric_only=True).max() -
                scoresDF.min(axis=0, numeric_only=True).min())*0.1
            )
        )
        plt.setp(axes.get_xticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor")
        axes.set_title("{} scores".format(self.object))
        plt.tight_layout()

        buf = io.BytesIO()
        try:
            plt.savefig(buf, format='png')
        except Exception as err:
            print("Couldn't generate the graph for {}".format(self.object))
            print(err)
        else:
            buf.seek(0)
            pltstring = base64.b64encode(buf.read())
            uri = urllib.parse.quote(pltstring)
            return uri

        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        view_title = "{} ({})".format(self.object, self.object.subject)
        context['view_title'] = view_title

        #context['graph'] = self.create_graph()
        graph = Graph(self.object)
        context['graph'] = graph.uri

        return context


class LessonCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/lesson_detail.html'

    model = Lesson
    form_class = forms.LessonForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        view_title = "New Lesson"

        if self.kwargs.get('subject_pk'):
            subject = get_object_or_404(Subject, pk=self.kwargs.get('subject_pk'))
            form = forms.LessonForm(initial={"name":"", "subject":subject})
            context['form'] = form

            view_title += " for {}".format(subject)

        context['view_title'] = view_title

        return context


class LessonUpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/lesson_form.html'

    form_class = forms.LessonForm
    model = Lesson
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_title = "Update {}".format(self.object)
        context["view_title"] = view_title
        return context
    

class LessonDeleteView(LoginRequiredMixin, generic.DeleteView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/lesson_form.html'

    model = Lesson
    success_url = reverse_lazy('teachadmin:subject_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_title = "Delete {}?".format(self.object)
        context["view_title"] = view_title
        return context
    

class LessonTestDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/lessontest_detail.html'

    template_name = 'teachadmin/lessontest_detail.html'
    context_object_name = 'lessontest'
    model = LessonTest

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.view_title = "{}".format(self.object)
        context['view_title'] = self.view_title

        graph = Graph(self.object)
        if graph.uri != False:
            context['graph'] = graph.uri

        return context


class LessonTestCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/lessontest_detail.html'

    model = LessonTest
    form_class = forms.LessonTestForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.view_title = "New lesson test"

        if self.kwargs.get('lesson_pk'):
            lesson = get_object_or_404(Lesson, pk=self.kwargs.get('lesson_pk'))
            form = forms.LessonTestForm(initial={"lesson":lesson})
            context['form'] = form
            context['lesson'] = lesson
            self.view_title += " for {}".format(lesson)
        
        context['view_title'] = self.view_title

        return context


class LessonTestUpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/lessontest_form.html'

    form_class = forms.LessonTestForm
    model = LessonTest
    context_object_name = 'lessontest'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_title = "Update {}".format(self.object)
        context["view_title"] = view_title
        return context

    
class LessonTestDeleteView(LoginRequiredMixin, generic.DeleteView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/lessontest_confirm_delete.html'

    model = LessonTest
    success_url = reverse_lazy('teachadmin:subject_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_title = "Delete {}".format(self.object)
        context["view_title"] = view_title
        return context
    

class LessonTestScoreDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/lessontest_detail.html'

    template_name = 'teachadmin/lessontestscore_detail.html'
    context_object_name = 'lessontestscore'
    model = LessonTestScore

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_title"] = "{}: {}({} points)".format(
            self.object.student,
            self.object.lessonTest,
            self.object.score)
        return context
    

class LessonTestScoreCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/lessontestscore_detail.html'

    model = LessonTestScore
    form_class = forms.LessonTestScoreForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        
        kwargs['subject'] = get_object_or_404(Subject, pk=self.kwargs.get('subject_pk'))
        kwargs['lessontest'] = get_object_or_404(LessonTest, pk=self.kwargs.get('lessontest_pk'))

        return kwargs


    def form_valid(self, form):
        if self.request.POST.get('students'):
            student = Student.objects.get(pk=self.request.POST.get('students'))
            form.instance.student = student

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.view_title = "New score"

        lessontest = get_object_or_404(LessonTest, pk=self.kwargs.get('lessontest_pk'))
        context['lessontest'] = lessontest
        
        self.view_title += " for {}".format(lessontest)

        context['view_title'] = self.view_title

        return context


class LessonTestScoreUpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/lessontestscore_form.html'

    form_class = forms.LessonTestScoreForm
    model = LessonTestScore
    context_object_name = 'lessontestscore'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_title = "Update {}".format(self.object)
        context["view_title"] = view_title
        return context


class LessonTestScoreDeleteView(LoginRequiredMixin, generic.DeleteView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/lessontestscore_confirm_delete.html'

    model = LessonTestScore
    success_url = reverse_lazy('teachadmin:subject_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_title = "Delete {} ({})".format(self.object, self.object.student)
        context["view_title"] = view_title
        return context
    

class OtherStudentsList(LoginRequiredMixin, generic.ListView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/other_students_list.html'

    template_name = 'teachadmin/other_students_list.html'
    context_object_name = 'other_students'

    def get_queryset(self):
        teacher = get_object_or_404(Teacher, user=self.request.user)
        homerooms = teacher.homeroom_set.all()
        subjects = teacher.subject_set.all()
        all_students = teacher.student_set.all()
        return all_students.exclude(homeroom__in=homerooms, subject__in=subjects)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = get_object_or_404(Teacher, user=self.request.user)
        context['teacher'] = teacher

        view_title = "Other students"
        context['view_title'] = view_title

        

        return context


class SchoolListView(LoginRequiredMixin, generic.ListView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/school_list.html'

    template_name = 'teachadmin/school_list.html'
    context_object_name = 'schools'

    def get_queryset(self):
        teacher = get_object_or_404(Teacher, user=self.request.user)
        return teacher.school_set.all()


class SchoolDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/school_detail.html'

    model = School
    template_name = 'teachadmin/school_detail.html'
    context_object_name = 'school'


class SchoolCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/school_detail.html'

    model = School
    form_class = forms.SchoolForm

    def form_valid(self, form):
        teacher = get_object_or_404(Teacher, user=self.request.user)
        school = form.save()
        teacher.school_set.add(school)
        return super().form_valid(form)


class SchoolUpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/school_detail.html'

    form_class = forms.SchoolForm
    model = School
    context_object_name = 'school'


class SchoolDeleteView(LoginRequiredMixin, generic.DeleteView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/school_list.html'

    model = School
    success_url = reverse_lazy('teachadmin:school_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        view_title = "Delete {}".format(self.object)
        context['view_title'] = view_title

        return context


class StudentView(generic.ListView):
    """ This is the ListView that shows a list of Students within a
            specific StudentClass """

    template_name = 'teachadmin/class_students.html'
    context_object_name = 'students_list'

    def get_class_graph(self):
        """ Function to generate and save a graph for use in template """
        studentClassTests = self.studentClass.studentclasstest_set.all()
        studentClassAssignments = self.studentClass.assignment_set.all()
        studentClassStudents = self.studentClass.student_set.all()

        scores = {}
        scores['Name'] = []
        scores['Gender'] = []
        student_numbers = []

        for count, student in enumerate(studentClassStudents):
            scores['Name'].append(student.first_name)
            scores['Gender'].append(student.gender)
            student_numbers.append(student.student_number)

            for test in studentClassTests.filter(studentClass=self.studentClass.id):
                if count == 0:
                    scores[f"{test.name}"] = []

                score = student.studentclasstestscore_set.filter(test=test.pk)[0]
                scores[f"{test.name}"].append(round(
                    (score.score / test.max_score)*100, 1))

            for assignment in studentClassAssignments.filter(studentClass=self.studentClass.id):
                if count == 0:
                    scores[f"{assignment.name}"] = []

                score = student.assignmentscore_set.filter(assignment=assignment.pk)[0]
                scores[f"{assignment.name}"].append(round(
                    (score.score / assignment.max_score)*100, 1))

        scoresDF = pd.DataFrame(scores, index=student_numbers)
        scoresDF.info()
        scoresDF.describe()

        fig = plt.figure()
        sns.set_style(style='darkgrid')
        sns.swarmplot(
            data=scoresDF,
            palette='deep')

        axes = fig.gca()
        axes.set_ylim(
            (scoresDF.min(axis=0, numeric_only=True).min())-3,
            (scoresDF.max(axis=0, numeric_only=True).max())+5
            )

        plt.setp(axes.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")
        axes.set_title("{} Test Data".format(self.studentClass))
        plt.tight_layout()

        # Getting the complete filepath to which we save the graph
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        static_dir = os.path.join(base_dir, 'teachadmin\\static\\teachadmin')
        fig_dir = os.path.join(static_dir, 'classes\\')

        plt.savefig('{}{}.png'.format(fig_dir, self.studentClass.name), format='png')
        plt.close(fig)

        return scoresDF

    def get_studentClass_comments(self, scoresDF: pd.DataFrame):
        """ This method is meant to take whatever scores-sheet is derived
            from the get_class_graph()-method and generate some general comments
            for each student based on how much they improved in each
            Test or Assignment"""

        advice_dict = {
            'English':'Should practice or study Family and Friends grammar points.',
            'Listening':'Should use the online resources from text books to help with pronunciation. YouTube also has many listening resources as well.',
            'Phonics':'Should review the vocabulary and grammar the sounds using Oxford’s app.',
            'Reading':'Should do plenty of reading this summer and practice answering questions about the story. YouTube has lots of read-alongside available.',
            'Behavior':'Should practice listening and following directions the first time. I know they will get better!',
            'Running Record':'Should do plenty of reading this summer and practice answering questions about the story. YouTube has lots of read-alongside available.'
        }
        skip_cats = ['Quiz', 'Homework']

        final_dict = {}
        for index, row in scoresDF.iterrows():
            final_dict[index] = {}
            final_dict[index]['Name'] = row['Name']
            final_dict[index]['Gender'] = row['Gender']
            col_dict = {}

            for col in scoresDF.iloc[:,2:].columns:
                colname, colnum = col[:-2], col[-1]

                if (colname not in skip_cats) and (int(colnum) == 1):
                    col_dict[colname] = 0
                    for num in range(2,6):
                        col_dict[colname] += (
                            row[f'{colname} {num}']-row[f'{colname} {num-1}']
                            )

            max_improve_cat_key = max(col_dict.keys(), key=(lambda k: col_dict[k]))
            min_improve_cat_key = min(col_dict.keys(), key=(lambda k: col_dict[k]))

            final_dict[index]['Max Category'] = {
                max_improve_cat_key:round(col_dict[max_improve_cat_key], 1)
            }
            final_dict[index]['Min Category'] = {
                min_improve_cat_key:round(col_dict[min_improve_cat_key], 1)
            }
            final_dict[index]['Growth'] = "{} has shown tremendous growth in {}".format(
                row['Name'], max_improve_cat_key
            )
            gender_pronoun = {'Female':'She', 'Male':'He'}
            final_dict[index]['Advice'] = (
                gender_pronoun[row['Gender']] + " " + advice_dict[min_improve_cat_key][0].lower() + advice_dict[min_improve_cat_key][1:]
            )

        for key, value in final_dict.items():
            print("\n", key)
            for cat, info in value.items():
                if isinstance(info,dict):
                    for infokey, infovalue in info.items():
                        print(cat, ":", infokey, "-", infovalue)
                else:
                    print(info)

        return final_dict

    def get_queryset(self):
        self.studentClass = get_object_or_404(
            StudentClass, pk=self.kwargs['student_class_id'])

        self.studentClass_size = len(
            Student.objects.filter(studentClass=self.studentClass))

        return Student.objects.filter(studentClass=self.studentClass)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_class'] = self.studentClass
        context['studentClass_size'] = self.studentClass_size

        # Creating the form for adding a new student to current StudentClass
        form = forms.StudentForm()
        # Creating the form for adding a new test(exam) to current StudentClass
        testform = forms.StudentClassTestForm()
        # Creating the form for adding new assignments to current StudentClass
        assignmentform = forms.AssignmentForm()

        # If the forms on the view are validated, the generated values
        # are printed to the console for confirmation
        if self.request.method == 'POST':
            form = forms.StudentForm(self.request.POST)
            testform = forms.StudentClassTestForm(self.request.POST)

            if form.is_valid():
                print("VALIDATION SUCCESS!")
                print("Name: \t" + form.cleaned_data['first_name'])
                print("Student #: \t" + form.cleaned_data['student_number'])

            elif testform.is_valid():
                print("VALIDATION SUCCESS!")
                print("Test Name: \t" + form.cleaned_data['test_name'])
                print("Min. Score: \t" + form.cleaned_data['min_score'])
                print("Max. Score: \t" + form.cleaned_data['max_score'])

        context['form'] = form
        context['testform'] = testform
        context['assignmentform'] = assignmentform

        # Creating a plot to clearly show scores of all students in a
        # specific StudentClass through Seaborn's 'lineplot'

        scoresDF = self.get_class_graph()
        context['min_max_dict'] = self.get_studentClass_comments(scoresDF)

        return context


class StudentListView(LoginRequiredMixin, generic.ListView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/student_list.html'
    
    template_name = 'teachadmin/student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        teacher = get_object_or_404(Teacher, user=self.request.user)
        return teacher.student_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        teacher = get_object_or_404(Teacher, user=self.request.user)
        context['teacher'] = teacher

        view_title = "All students"
        context['view_title'] = view_title

        return context


class StudentDetailView(LoginRequiredMixin, generic.DetailView):
    """ This DetailView gets called whenever you click
        on a specific student to show their details """

    model = Student
    context_object_name = 'student'
    template_name = 'teachadmin/student_detail.html'


    # Re-write this method
    def get_student_graph(self):
        all_scores = {}
        all_scores_index = []
        for score in self.exam_scores:
            exam_title = score.exam.name[:-2]
            if '1' in score.exam.name:
                all_scores[exam_title] = []

            all_scores[exam_title].append(int((
                score.score/score.exam.max_score
                )*100))

        print(all_scores)

        col_length = []
        for test in all_scores:
            col_length.append(len(all_scores[test]))

        all_scores_index.append(list(range(max(col_length))))
        print(all_scores_index)

        scoresDF = pd.DataFrame(all_scores, index=all_scores_index)

        scoresDF.info()
        print(scoresDF)

        # Setting up a figure to plot on
        fig = plt.figure()
        # For consistency, same style as the class-graph is used
        sns.set_style(style='darkgrid')
        # Palette of the plot is also set to be the same
        sns.catplot(data=scoresDF, palette='deep')
        # Get the axes from current figure
        axes = fig.gca()
        # Setting y-limits based on the min and max values from DataFrame
        axes.set_ylim(
            (scoresDF.min(axis=0, numeric_only=True).min())-2,
            102
        )
        # Based on the Series in the DataFrame, we set labels for the graph
        # and tilt them slightly for visibility
        plt.setp(axes.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")
        # Last but not least, setting title for the figure and adjusting
        # for small padding spaces (risk of labels or title being cut)
        axes.set_title("{} Test Data".format(self.object))
        plt.tight_layout()

        # Getting the complete filepath to which we save the graph
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        static_dir = os.path.join(base_dir, 'teachadmin\\static\\teachadmin')
        fig_dir = os.path.join(static_dir, 'students\\')

        file_exists = os.path.exists(
            fig_dir+'{}.png'.format(self.object.pk)
            )

        print(file_exists)

        if not file_exists:
            plt.savefig(
                fig_dir+'{}.png'.format(self.object.pk),
                format='png')
        else:
            time_in_seconds = os.path.getmtime(
                fig_dir+'{}.png'.format(self.object.pk)
                )
            file_date = datetime.fromtimestamp(time_in_seconds)
            right_now = datetime.now()
            time_diff = right_now - file_date

            print((time_diff.seconds)/60, " minutes")

            if time_diff.seconds >= (15*60):
                plt.savefig(
                    fig_dir+'{}.png'.format(self.object.pk),
                    format='png')
                print("\n\nStudent Graph File updated!\n")

        plt.close(fig)

        return file_exists

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.exam_scores = ExamScore.objects.filter(
            student=self.object
        )
        self.assignment_scores = AssignmentScore.objects.filter(
            student=self.object
        )
        context['exam_scores'] = self.exam_scores
        context['assignment_scores'] = self.assignment_scores

        if self.exam_scores.count() > 0 and self.assignment_scores.count() > 0:
            pass
            # Re-write the method
            #context['file_exists'] = self.get_student_graph()    

        if self.object.subject != None:
            context['subjects'] = self.object.subject.all()


        return context


class StudentCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = 'teachadmin/login'
    redirect_field_name = 'teachadmin/student_detail.html'

    model = Student
    form_class = forms.StudentForm

    def form_valid(self, form):
        teacher = get_object_or_404(Teacher, user=self.request.user)
        
        if self.request.POST.get('selected_homeroom') != "":
            form.instance.homeroom = HomeRoom.objects.get(
                pk=self.request.POST.get('selected_homeroom')
            )

        student = form.save()
        teacher.student_set.add(student)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.view_title = 'Add Student'
        context['view_title'] = self.view_title

        teacher = get_object_or_404(Teacher, user=self.request.user)
        if teacher.has_homeroom():
            homerooms = teacher.homeroom_set.all()
            context['homerooms'] = homerooms
        
        context['teacher'] = teacher

        return context


class StudentUpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/student_form.html'

    form_class = forms.StudentForm
    model = Student
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_title = "Update {}".format(self.object)

        teacher = get_object_or_404(Teacher, user=self.request.user)
        if teacher.has_homeroom():
            homerooms = teacher.homeroom_set.all()
            context['homerooms'] = homerooms

        context['teacher'] = teacher

        context["view_title"] = view_title
        return context


class StudentDeleteView(LoginRequiredMixin, generic.DeleteView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/student_confirm_delete.html'

    model = Student
    success_url = reverse_lazy('teachadmin:student_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_title = "Delete {}".format(self.object)
        context["view_title"] = view_title
        return context


class SubjectListView(LoginRequiredMixin, generic.ListView):
    """ Subject List View """
    
    template_name = 'teachadmin/subject_list.html'
    context_object_name = 'subjects'

    def get_queryset(self):
        teacher = get_object_or_404(Teacher, user=self.request.user)
        return teacher.subject_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SubjectDetailView(LoginRequiredMixin, generic.DetailView):
    """ Subject Detail View """
    model = Subject
    context_object_name = 'subject'
    template_name = 'teachadmin/subject_detail.html'

    def create_graph(self):
        students = self.object.student_set.all()
        exams = self.object.exam_set.all()
        assignments = self.object.assignment_set.all()
        lessons = self.object.lesson_set.all()
        lessontests = LessonTest.objects.filter(lesson__in=lessons)
        homeworks = Homework.objects.filter(lesson__in=lessons)

        index = []
        scoreDict = {}
        scoreDict['Student'] = []
        scoreDict['Gender'] = []

        for exam in exams:
            scoreDict['{}({})'.format(exam, exam.pk)] = []
        for assignment in assignments:
            scoreDict['{}({})'.format(assignment, assignment.pk)] = []
        for lessontest in lessontests:
            scoreDict['{}({})'.format(lessontest, lessontest.pk)] = []
        for homework in homeworks:
            scoreDict['{}({})'.format(homework, homework.pk)] = []

        for count, student in enumerate(students):
            studentScores = {}
            for exam in exams:
                if '{}({})'.format(exam, exam.pk) not in studentScores.keys():
                    studentScores['{}({})'.format(exam, exam.pk)] = []
                if exam.examscore_set.filter(student=student).count() >=1:
                    for examscore in exam.examscore_set.filter(student=student):
                        studentScores['{}({})'.format(exam, exam.pk)].append(
                            round(((examscore.score/exam.max_score)*100),1)
                        )
                else:
                    studentScores['{}({})'.format(exam, exam.pk)].append(None)
            
            for assignment in assignments:
                if '{}({})'.format(assignment, assignment.pk) not in studentScores.keys():
                    studentScores['{}({})'.format(assignment, assignment.pk)] = []
                if assignment.assignmentscore_set.filter(student=student).count() >= 1:
                    for assignmentscore in assignment.assignmentscore_set.filter(student=student):
                        studentScores['{}({})'.format(assignment, assignment.pk)].append(
                            round(((assignmentscore.score/assignment.max_score)*100),1)
                        )
                else:
                    studentScores['{}({})'.format(assignment, assignment.pk)].append(None)

            for lessontest in lessontests:
                if '{}({})'.format(lessontest, lessontest.pk) not in studentScores.keys():
                    studentScores['{}({})'.format(lessontest, lessontest.pk)] = []
                if lessontest.lessontestscore_set.filter(student=student).count() >= 1:
                    for lessontestscore in lessontest.lessontestscore_set.filter(student=student):
                        studentScores['{}({})'.format(lessontest, lessontest.pk)].append(
                            round(((lessontestscore.score/lessontest.max_score)*100), 1)
                        )
                else:
                    studentScores['{}({})'.format(lessontest, lessontest.pk)].append(None)

            for homework in homeworks:
                if '{}({})'.format(homework, homework.pk) not in studentScores.keys():
                    studentScores['{}({})'.format(homework, homework.pk)] = []
                if homework.homeworkscore_set.filter(student=student).count() >= 1:
                    for homeworkscore in homework.homeworkscore_set.filter(student=student):
                        studentScores['{}({})'.format(homework, homework.pk)].append(
                            round(((homeworkscore.score/homework.max_score)*100), 1)
                        )
                else:
                    studentScores['{}({})'.format(homework, homework.pk)].append(None)
            
            for key in studentScores.keys():
                scoreDict[key].append(max(studentScores[key]))

            index.append(count)
            scoreDict['Student'].append(str(student))
            scoreDict['Gender'].append(student.gender)
        
        keylist = []
        for key in scoreDict.keys():
            if all(elem == None for elem in scoreDict[key]):
                keylist.append(key)
        
        for key in keylist:
            scoreDict.pop(key)

        scoreDF = pd.DataFrame(data=scoreDict, index=index)
        checkDF = scoreDF.iloc[:,2:]

        if checkDF.empty == False:
            scoreDF['Gender'] = scoreDF['Gender'].apply(gender_map)

            fig = plt.figure()
            sns.set_style(style='darkgrid')
            plt.style.use("dark_background")
            sns.swarmplot(
                data=scoreDF,
                palette='bright')

            axes = fig.gca()
            margin = int(
                (scoreDF.max(axis=0, numeric_only=True).max() -
                scoreDF.min(axis=0, numeric_only=True).min())*0.1
            )
            axes.set_ylim(
                (scoreDF.min(axis=0, numeric_only=True).min())-margin,
                (scoreDF.max(axis=0, numeric_only=True).max())+margin
            )

            plt.setp(axes.get_xticklabels(), rotation=45, ha="right",
                        rotation_mode="anchor")
            axes.set_title("{} scores".format(self.object))
            plt.tight_layout()

            # To save space on the server, I convert the graph into 64-bit data and
            # put it into a local memory buffert from which the img-tag reads the data
            # and displays the graph
            buf = io.BytesIO()
            fig = plt.gcf()
            try:
                plt.savefig(buf, format='png')
                buf.seek(0)
                figstring = base64.b64encode(buf.read())
                uri = urllib.parse.quote(figstring)
            except Exception as err:
                print("Error while processing data for {}".format(self.object))
                print(err)
            else:
                plt.close(fig)
                return uri
        else:
            return False


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = get_object_or_404(Teacher, user=self.request.user)
        context['teacher'] = teacher

        if self.object.school != None:
            view_title = "{} ({})".format(self.object, self.object.school)
        else:
            view_title = "{}".format(self.object)

        context['view_title'] = view_title

        #context['graph'] = self.create_graph()
        graph = Graph(self.object)
        context['graph'] = graph.uri

        return context


class SubjectCreateView(LoginRequiredMixin, generic.CreateView):
    """ Standard CreateView class for Subjects """
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/subject_detail.html'

    model = Subject

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('student_pk') != None:
            self.form_class = forms.SubjectToStudentForm
        else:
            self.form_class = forms.SubjectForm

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        teacher = get_object_or_404(Teacher, user=self.request.user)
        subject = form.save()
        subject.teacher.add(teacher)
        
        if self.form_class == forms.SubjectToStudentForm:
            student = Student.objects.get(pk=self.kwargs['student_pk'])
            subject.student_set.add(student)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.form_class == forms.SubjectToStudentForm:
            student = get_object_or_404(Student, pk=self.kwargs['student_pk'])
            context['student'] = student
            
            self.view_title = 'Add subject for {}'.format(student.first_name)
        else:
            self.view_title = 'Add Subject'
        
        context['title'] = self.view_title
        
        return context
    
    def get_success_url(self):
        if self.form_class == forms.SubjectToStudentForm:
            return reverse('teachadmin:student_detail', kwargs={'pk':self.kwargs['student_pk']})
        return super().get_success_url()


class SubjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = "teachadmin/login/"
    redirect_field_name = "teachadmin/subject_update.html"

    model = Subject
    form_class = forms.SubjectForm

    template_name = "teachadmin/subject_update.html"
    context_object_name = "subject"

    def form_valid(self, form):
        subject = form.save()
        students = Student.objects.filter(pk__in=self.request.POST.getlist('added_students'))
        for student in students:
            subject.student_set.add(student)
            
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        self.teacher = get_object_or_404(Teacher, user=self.request.user)
        context['teacher'] = self.teacher

        self.view_title = 'Edit Subject'
        context['view_title'] = self.view_title

        if self.object.student_set.all() != None:
            self.subject_students = self.object.student_set.all()
            context['subject_students'] = self.subject_students

        return context


class SubjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Subject
    success_url = reverse_lazy('teachadmin:subject_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['view_title'] = "Delete {}?".format(self.object)

        return context


class TeacherDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = 'teachadmin/login/'
    redirect_field_name = 'teachadmin/teacher_detail.html'

    context_object_name = 'teacher'
    model = Teacher
    template_name = "teachadmin/teacher_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['homerooms'] = HomeRoom.objects.filter(
            teacher=self.kwargs['pk'])
        return context


@login_required
def teachadmin_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def teachadmin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("Account Not Active")
        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied!")
    else:
        return render(request,'teachadmin/login.html',{})

def register(request):
    registered = False
    
    if request.method == "POST":
        user_form = forms.UserForm(data=request.POST)
        teacher_form = forms.TeacherForm(data=request.POST)

        if user_form.is_valid() and teacher_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            teacher = teacher_form.save(commit=False)
            teacher.user = user

            if 'profile_pic' in request.FILES:
                teacher.profile_pic = request.FILES['profile_pic']

            teacher.save()

            registered = True
        else:
            print(user_form.errors, teacher_form.errors)
    else:
        user_form = forms.UserForm()
        teacher_form = forms.TeacherForm()

    return render(request, 'teachadmin/registration.html',
                            {'user_form':user_form,
                                'teacher_form':teacher_form,
                                'registered':registered})

def addStudent(request, student_group_id):

    if request.method == 'POST':
        student_group = get_object_or_404(StudentClass, pk=student_group_id)
        student, created = Student.objects.get_or_create(
                                first_name=request.POST['first_name'],
                                student_number=request.POST['student_number'],
                                studentClass=student_group)
        if not created:
            raise Http404('The student {} in current class already exists.\
                            '.format(request.POST['first_name']))
        else:
            return HttpResponseRedirect(reverse('teachadmin:studentsView',
                                                args=(student_group.pk,)))

    else:
        raise Http404('Do not try to hack my shit! A-hole!')

def addStudentClass(request):
    if request.method == 'POST':
        form = forms.StudentClassForm(request.POST)
        if form.is_valid():
            """ This will be executed when user uploads a file to add
                    StudentClass"""

            school = get_object_or_404(School, pk=form.cleaned_data['school'].pk)
            studentClass, created = StudentClass.objects.get_or_create(
                school=school,
                name=form.cleaned_data['name'],
                grade=form.cleaned_data['grade']
            )
            if request.FILES.get('classFile', False):

                try:
                    # Loading the file's data directly into a Pandas DataFrame
                    results = pd.read_csv(request.FILES['classFile'],
                                                index_col = 'Number')
                except Exception as err:
                    print("ERROR: Couldn't read file into pandas's CSV-format.")
                    print(err)
                    raise Http404('ERROR: Not able to read CSV-file')
                else:
                    # Since we will create classes, tests, students, and scores
                    # separately, we separate the data into relevant data for
                    # students and [tests + scores] respectively
                    results.info()
                    results_students = results.loc[:,['Name','Gender']]
                    results_students.info()
                    results.drop(columns=['Name','Gender'], inplace=True)
                    results.info()
                    results.astype('int64', copy=False)

                    for row in results_students.itertuples():
                        """ Iterate through the smaller DataFrame to get each
                            student's data to store in the database """

                        student, created = Student.objects.get_or_create(
                            student_number=row.Index,
                            first_name=row.Name,
                            gender=row.Gender
                        )
                        if not created:
                            print("{} student {} with number {} exists".format(
                                row.Gender,
                                row.Name,
                                row.Index
                            ))

                        student.studentClass.add(studentClass)

                        for col in results.columns:
                            if ':' in col:
                                colname = col.split(':')[0]

                                test_score_limits = col.split(':')[1]
                                test_min_score = int(test_score_limits.split('-')[0])
                                test_max_score = int(test_score_limits.split('-')[1])

                                studentClassTest, created = StudentClassTest.objects.get_or_create(
                                    name=colname,
                                    min_score=test_min_score,
                                    max_score=test_max_score
                                )

                                studentClassTest.studentClass.add(studentClass)

                                studentClassTestScore, created = StudentClassTestScore.objects.get_or_create(
                                    student=student,
                                    test=studentClassTest,
                                    score=int(results.loc[row.Index, col])
                                )

                finally:
                    return HttpResponseRedirect(reverse('teachadmin:index'))

    else:
        return render(request, 'teachadmin/index.html')

def addStudentToHomeRoom(request, homeroom_pk, teacher_pk):
    if request.method == 'POST':
        studentform = forms.StudentToHomeRoomForm(request.POST)
        if studentform.is_valid():
            current_homeroom = get_object_or_404(HomeRoom, pk=homeroom_pk)
            current_teacher = get_object_or_404(Teacher, pk=teacher_pk)
            
            student = studentform.save()

            current_homeroom.student_set.add(student)
            current_teacher.student_set.add(student)
            
            student.save()

    return HttpResponseRedirect(reverse('teachadmin:homeroom_detail', kwargs={'pk':homeroom_pk}))

def addSchool(request):
    if request.method == 'POST':
        schoolform = forms.SchoolForm(request.POST)
        if schoolform.is_valid():
            school = schoolform.save()
            teacher = Teacher.objects.get(
                user=request.user
            )
            teacher.school_set.add(school)
            school.save()

    return HttpResponseRedirect(reverse('teachadmin:index'))

def addTest(request, student_class_id):
    if request.method == 'POST':
        form = forms.StudentClassTestForm(request.POST)
        if form.is_valid():
            # Getting the current StudentClass form the database
            student_class = get_object_or_404(StudentClass, pk=student_class_id)
            # Initially omitting the StudentClass object from the creation
            # of the StudentClassTest object as it is a ManyToManyField
            test, created = StudentClassTest.objects.get_or_create(
                                name=request.POST['name'],
                                min_score=request.POST['min_score'],
                                max_score=request.POST['max_score'])

            if not created:
                raise Http404('There already exists another identical test in \
                                current StudentClass.')
            else:
                # ManyToManyFields need to have their data added AFTER the
                # main object is saved to the database / created
                test.studentClass.add(student_class)
                return HttpResponseRedirect(reverse('teachadmin:studentsView',
                                                    args=(student_class.pk,)))

def addAssignment(request, student_class_id):

    # Getting current StudentClass from the database
    studentClass = get_object_or_404(StudentClass, pk=student_class_id)

    if request.method == 'POST':
        print("\n", "Request method: POST", "\n")
        if request.FILES.get('assignmentFile', False):
            try:
                print("\n", "Reading CSV", "\n")
                assignmentDF = pd.read_csv(
                    request.FILES['assignmentFile'],
                    index_col = 'Number')
                assignmentDF.head()
            except Exception as err:
                print("\n \
                    Couldn't read CSV-file data into Pandas's DataFrame-format\
                    \n")
                print(err)
                raise Http404("Couldn't read CSV-file data \
                    into Pandas's DataFrame-format")
            else:
                print("Reading CSV successful!", "\n")
                assignment_studentsDF = assignmentDF.loc[:,['Name','Gender']]

                assignmentDF.drop(columns=['Name','Gender'], inplace=True)
                assignmentDF = assignmentDF.round(0).astype('int64')

                for row in assignment_studentsDF.itertuples():
                    """ Iterate through the smaller DataFrame to get each
                    student's data to store in/load from the database """
                    student, created = Student.objects.get_or_create(
                        studentClass=studentClass,
                        student_number=row.Index,
                        first_name=row.Name,
                        gender=row.Gender
                    )
                    if not created:
                        print("Student {} already exists in class {}".format(
                            row.Name,
                            studentClass
                        ))
                    for col in assignmentDF.columns:
                        colname = col.split(":")[0]

                        assignment_score_limits = col.split(":")[1]
                        assignment_min_score = int(assignment_score_limits.split("-")[0])
                        assignment_max_score = int(assignment_score_limits.split("-")[1])

                        print("Attmepting to Assignment: ",
                            colname,
                            assignment_min_score,
                            assignment_max_score,
                            sep="\n")
                        assignment, created = Assignment.objects.get_or_create(
                            name=colname,
                            min_score=assignment_min_score,
                            max_score=assignment_max_score
                        )
                        print("Attempting to AssignmentScore: ",
                            student,
                            assignment,
                            int(assignmentDF.loc[row.Index, col]),
                            sep="\n")
                        assignmentscore, created = AssignmentScore.objects.get_or_create(
                            student=student,
                            assignment=assignment,
                            score=int(assignmentDF.loc[row.Index, col])
                        )
        else:
            print("\nFile not found.\n")

    return HttpResponseRedirect(reverse('teachadmin:studentsView',
                                                    args=(studentClass.pk,)))


def gender_map(gender):
    if gender == 'F':
        return 'Female'
    elif gender == 'M':
        return 'Male'
    else:
        return 'Other'
