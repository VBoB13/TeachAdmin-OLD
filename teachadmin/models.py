from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import datetime

# Create your models here.

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional Info
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='teachers/profile_pics/', blank=True)
    country = CountryField(blank=True, blank_label='(Select country)', help_text="Optional.")

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("teacher_detail", kwargs={"pk": self.pk})

    def has_homeroom(self):
        return self.homeroom_set.all().exists()
    

class School(models.Model):
    name = models.CharField(max_length=256, help_text="Up to 256 characters")
    teacher = models.ManyToManyField(Teacher)
    address = models.CharField(
        max_length=200,
        blank=True,
        help_text="(Optional) English, please...")

    class Meta:
        ordering = [
            'name',
        ]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("teachadmin:school_detail", kwargs={"pk":self.pk})


class HomeRoom(models.Model):
    name = models.CharField(max_length=50, help_text="Anything within 50 characters.")
    teacher = models.ManyToManyField(Teacher)
    school = models.ForeignKey(School, on_delete=models.CASCADE, help_text="Choose one.")
    grade = models.PositiveSmallIntegerField(blank=True, null=True, help_text="Positive numbers.")
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = [
            'name',
            'grade',
            'school',
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("teachadmin:homeroom_detail",
            kwargs={
                "pk": self.pk
                })

    def students(self, as_list:bool=False):
        """ Returns a QuerySet of all the students linked to the current HomeRoom. 
            If none are found, this returns False.
            Setting as_list=True will return a list of the students' full names.
            params: as_list(bool)=False
            OUTPUT: QuerySet, List or False"""
        qs = self.student_set.all()
        if qs.exists():
            if as_list:
                return ["{} {}".format(
                    student.first_name, student.last_name
                ) for student in qs]
            return qs
        return False
    
    def subjects(self):
        """ Returns a QuerySet of all the subjects linked to the current HomeRoom. """
        qs = self.subject_set.all()
        if qs.exists():
            return qs
        return False

    def get_score_models(self, as_tuples:bool=False):
        """ Returns a list of score models (Exam, Assignment, LessonTest, Homework)
            that are linked to the current HomeRoom """
        score_model_list = []
        qs = self.subjects()
        if qs:
            for subject in qs:
                if as_tuples:
                    score_model_list.extend(
                        subject.get_score_models(as_tuples=True)
                    )
                else:
                    score_model_list.extend(subject.get_score_models())
        return score_model_list


class Subject(models.Model):
    name = models.CharField(max_length=50, help_text="Anything within 50 characters.")
    teacher = models.ManyToManyField(Teacher)
    school = models.ForeignKey(School, blank=True, null=True, on_delete=models.CASCADE)
    homeroom = models.ManyToManyField(HomeRoom)
    description = models.TextField(
        max_length=250,
        blank=True,
        null=True)

    class Meta:
        ordering = [
            'name',
            'school'
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("teachadmin:subject_detail", kwargs={"pk": self.pk})
    
    def clean(self):
        teacher = self.teacher.first()
        if teacher.subject_set.filter(name__iexact=self.name).exists():
            raise ValidationError({
                "name": ValidationError(_("You already have a subject by this name. Choose another one!"), code='invalid')
            })
        if self.description == "":
            self.description = None

    def has_exam(self):
        return self.exam_set.all().exists()

    def get_exams(self):
        """ Model method that retrieves all the related Exams for the current Subject.
            If no Exams are found, it returns False
            PARAMS: None
            RETURNS: QuerySet / False """
        qs = self.exam_set.all()
        if qs.exists():
            return qs
        return False
    
    def has_assignment(self):
        return self.assignment_set.all().exists()

    def get_assignments(self):
        """ Model method that retrieves all the related Assignments for the current Subject.
            If no Exams are found, it returns False
            PARAMS: None
            RETURNS: QuerySet / False """
        qs = self.assignment_set.all()
        if qs.exists():
            return qs
        return False
    
    def has_lesson(self):
        return self.lesson_set.all().exists()

    def get_lessons(self):
        """ Model method that retrieves all the related Lessons for the current Subject.
            If no Exams are found, it returns False
            PARAMS: None
            RETURNS: QuerySet / False """
        qs = self.lesson_set.all()
        if qs.exists():
            return qs
        return False
    
    def students(self, as_list:bool=False):
        """ Attempts to retrieve the students registered at the current Subject.
            Failure to do so will return False instead.
            params: as_list (bool)=False
            OUTPUT: QuerySet, List or False """
        qs = self.student_set.all()
        if qs.exists():
            if as_list:
                return [
                    "{} {}".format(
                        student.first_name, student.last_name
                        ) for student in qs]
            return qs
        return False

    def get_score_models(self, as_tuples:bool = False):
        score_models = []
        
        exam_qs = self.get_exams()
        if exam_qs:
            for exam in exam_qs:
                score_models.append(exam)

        assignment_qs = self.get_assignments()
        if assignment_qs:
            for assignment in assignment_qs:
                score_models.append(assignment)
            
        lesson_qs = self.get_lessons()
        if lesson_qs:
            for lesson in lesson_qs:
                lesson_models_list = lesson.get_score_models()
                score_models.extend(lesson_models_list)
        
        if as_tuples:
            return [(self, model) for model in score_models]
        return score_models


class Exam(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Anything within 100 characters.")
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE)
    max_score = models.PositiveSmallIntegerField(
        default=100,
        help_text="Default: 100")
    min_score = models.PositiveSmallIntegerField(
        default=0,
        help_text="Default: 0")
    date = models.DateField(
        blank=True,
        default=datetime.date.today,
        help_text="Format: YYYY-MM-DD")

    class Meta:
        ordering = [
            'date',
            'name',
            'subject',
        ]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("teachadmin:exam_detail", kwargs={
            "subject_pk": self.subject.pk,
            "pk": self.pk
            })

    def clean(self):
        all_exams_in_subject = self.subject.exam_set.all()
        for exam in all_exams_in_subject:
            if not self.pk and self.name == exam.name:
                raise ValidationError({
                    "name": ValidationError(_("The exam name already exists in this subject."), code='invalid')
                })
        if self.max_score < self.min_score:
            raise ValidationError(_("Maximum score cannot be lower than minimum score!"))

    def has_score(self):
        return self.examscore_set.all().exists()
    
    def students(self):
        """ Returns a list of UNIQUE students that has scores for the current exam. """

        if self.has_score():
            students = []
            scores = self.examscore_set.all().select_related('student')
            for score in scores:
                if score.student not in students:
                    students.append(score.student)
            return students
        else:
            return False

    def scores(self):
        return self.examscore_set.all().select_related('student')


class Lesson(models.Model):
    name = models.CharField(
        max_length=30,
        help_text="Within 30 characters.")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    start_date = models.DateField(
        verbose_name="Start date",
        null=True,
        default=datetime.date.today,
        help_text="Format: YYYY-MM-DD"
    )
    end_date = models.DateField(
        verbose_name="End date",
        null=True,
        blank=True,
        help_text="Format: YYYY-MM-DD"
    )

    class Meta:
        ordering = [
            'name',
            'start_date',
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("teachadmin:lesson_detail", kwargs={
            "pk": self.pk,
            "subject_pk": self.subject.pk
            })

    def has_lessontest(self):
        """ If the Lesson has any tests, it returns True. Otherwise, it returns False.
            INPUT: None
            OUTPUT: bool """
        return self.lessontest_set.all().exists()

    def get_lessontests(self):
        """ Attempts to retrieve all LessonTests associated with the current Lesson.
            If none are found, it will return False.
            PARAMS: None
            OUTPUT: QuerySet / False """
        qs = self.lessontest_set.all()
        if qs.exists():
            return qs
        return False
    
    def has_homework(self):
        """ If the Lesson has any homeworks, it returns True. Otherwise, it returns False.
            INPUT: None
            OUTPUT: bool """
        return self.homework_set.all().exists()

    def get_homeworks(self):
        """ Attempts to retrieve all Homeworks associated with the current Lesson.
            If none are found, it will return False.
            PARAMS: None
            OUTPUT: QuerySet / False """
        qs = self.homework_set.all()
        if qs.exists():
            return qs
        return False
    
    def get_score_models(self, as_tuples:bool=False):
        """ This method looks up whether there are any tests or homeworks for the current lesson.
            If there are, it returns a list of the tests and homeworks.
            Returns a list of LessonTests and Homeworks (respectively)
            INPUT: None
            OUTPUT: list [LessonTest-1, LessonTest-2, Homework-1 ... ModelObject-N] """

        test_hw_list = []
        
        lessontests = self.get_lessontests()
        homeworks = self.get_homeworks()
        if lessontests:
            for test in lessontests:
                if test.has_score():
                    test_hw_list.append(test)
        if homeworks:
            for homework in homeworks:
                if homework.has_score():
                    test_hw_list.append(homework)

        if as_tuples:
            return [(self, model) for model in test_hw_list]
        return test_hw_list

    def students(self):
        return self.subject.students()


class LessonTest(models.Model):
    name = models.CharField(
        max_length=50,
        help_text="Within 50 characters.")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    max_score = models.PositiveSmallIntegerField(
        default=100,
        help_text="Default: 100")
    min_score = models.PositiveSmallIntegerField(
        default=0,
        help_text="Default: 0")
    test_date = models.DateField(
        default=datetime.date.today(),
        blank=True,
        help_text="Format: yyyy-mm-dd")

    class Meta:
        ordering = [
            'name',
            'test_date',
            'lesson',
        ]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse(
            "teachadmin:lessontest_detail",
            kwargs={
                "subject_pk":self.lesson.subject.pk,
                "lesson_pk":self.lesson.pk,
                "pk": self.pk
                })

    def clean(self):
        if self.lesson.lessontest_set.filter(name__iexact=self.name).exists():
            raise ValidationError({
                "name": ValidationError(_(
                    "Lesson test with name {} already exists in {}. Please choose another name.").format(
                    self.name, self.lesson), 
                    code='invalid')
            })
        if self.min_score > self.max_score:
            raise ValidationError({
                "max_score": ValidationError(_("Minimum score cannot be higher than maximum score."), code='invalid')
            })


    def has_score(self):
        """ Checks whether the LessonTest has any test scores associated with it.
            INPUT: None
            OUTPUT: bool """
        return self.lessontestscore_set.all().exists()
    
    def students(self):
        """ Returns list of UNIQUE students that has scores for the current test.
            If there are no scores for the test, it will return False.
            params: None
            OUTPUT: list / False """
        qs = self.lessontestscore_set.select_related('student').order_by('student', 'score').distinct('student')
        if qs.exists():
            students = []
            for score in qs:
                students.append(score.student)
            return students
        return []

    def scores(self):
        """ Attempts to retrieve all of the related LessonTestScores to the current LessonTest.
            If none are found, it returns False.
            PARAMS: None
            OUTPUT: LessonTestScores (QuerySet) / False (bool) """
        qs = self.lessontestscore_set.all().select_related('student')
        if qs.exists():
            return qs
        return False


class Student(models.Model):
    first_name = models.CharField(
        max_length=50,
        help_text="Within 50 characters.")
    last_name = models.CharField(
        max_length=50,
        blank=True,
        default="",
        help_text="Within 50 characters.")
    student_number = models.CharField(
        max_length=20,
        blank=True,
        default="",
        help_text="Within 20 characters.")
    homeroom = models.ForeignKey(
        HomeRoom,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text="Optional.")
    subject = models.ManyToManyField(Subject)
    teacher = models.ManyToManyField(Teacher)
    
    FEMALE = 'F'
    MALE = 'M'
    OTHER = 'O'
    GENDERS_CHOICES = [
        (FEMALE, 'Female'),
        (MALE, 'Male'),
        (OTHER, 'Other'),
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDERS_CHOICES,
        default=FEMALE
    )

    class Meta:
        ordering = [
            'first_name',
            'last_name',
            'student_number'
        ]

    def __str__(self):
        if len(self.last_name) == 0:
            return self.first_name
        else:
            return "{} {}".format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse("teachadmin:student_detail", kwargs={"pk": self.pk})

    def clean(self):
        if self.last_name == None:
            self.last_name = ""


class Assignment(models.Model):
    name = models.CharField(max_length=50)
    max_score = models.PositiveSmallIntegerField(default=100)
    min_score = models.PositiveSmallIntegerField(default=0)
    deadline = models.DateTimeField(
        default=timezone.now,
        help_text="Format: YYYY-MM-DD HH:MM:SS")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    creator = models.ManyToManyField(Teacher)

    class Meta:
        ordering = [
            'name',
            'deadline',
            'subject',
        ]

    def get_absolute_url(self):
        return reverse("teachadmin:assignment_detail",
            kwargs={
                "subject_pk": self.subject.pk,
                "pk": self.pk}
            )

    def __str__(self):
        return "{}".format(self.name)

    def has_score(self):
        return self.assignmentscore_set.all().exists()
    
    def students(self):
        """ Returns UNIQUE students that has scores for the current test. """

        if self.has_score():
            students = []
            scores = self.assignmentscore_set.all().select_related('student')
            for score in scores:
                if score.student not in students:
                    students.append(score.student)
            return students
        return []

    def scores(self):
        """ Returns all the scores associated with the current test. """
        return self.assignmentscore_set.all().select_related('student')


class AssignmentScore(models.Model):
    score = models.PositiveSmallIntegerField()
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    turn_in_time = models.DateTimeField(
        default=timezone.now,
        help_text="Format: YYYY-MM-DD HH:MM:SS")

    class Meta:
        ordering = [
            'assignment',
            'turn_in_time',
            'score',
            ]

    def __str__(self):
        if self.assignment.min_score == 0 and self.assignment.max_score == 100:
            return "{}".format(self.score)
        else:
            return "{} ({}%)".format(self.score,
                round((self.score/self.assignment.max_score)*100,1))

    def clean(self):
        # Don't allow for scores higher than the Assignment's max_score field
        if self.score > self.assignment.max_score:
            raise ValidationError({
                "score": ValidationError(_("Score cannot be higher than the assignment's maximum score."), code='invalid')
            })
        if self.score < self.assignment.min_score:
            raise ValidationError({
                "score": ValidationError(_("Score cannot be lower than the assignment's minimum score."), code='invalid')
            })


class ExamScore(models.Model):
    score = models.PositiveSmallIntegerField(default=0)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = [
            'exam',
            'timestamp',
            'score',
            'student',
        ]

    def __str__(self):
        return "{}".format(self.score)

    def get_absolute_url(self):
        return reverse("teachadmin:exam_detail", kwargs={
            "pk": self.exam.pk,
            "subject_pk": self.exam.subject.pk
            })

    def clean(self):
        # First we check to see whether the chosen student DOES NOT have any scores for the exam
        if self.student not in self.exam.students():
        # Do not allow scores to be set higher than exam's max_score
            if self.score > self.exam.max_score:
                raise ValidationError({
                    "score": ValidationError(
                        _("Score cannot be higher than exam's maximum score."),
                        code='invalid'
                        )
                    })
            if self.score < self.exam.min_score:
                raise ValidationError({
                    "score": ValidationError(
                        _("Score cannot be lower than exam's minimum score."),
                        code='invalid'
                        )
                    })
        else:
            exam_scores = self.exam.scores().filter(student=self.student).select_related('student')
            if exam_scores.count() > 0:
                for score in exam_scores:
                    if score.score > self.score:
                        raise ValidationError({
                            "score": ValidationError(
                                _("{} already has a higher score than you tried to enter: {} > {} ".format(
                                score.student, score.score, self.score)), code='invalid')
                            })
                    

class LessonTestScore(models.Model):
    score = models.PositiveSmallIntegerField(default=0)
    lessonTest = models.ForeignKey(LessonTest, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        ordering = [
            'lessonTest',
            'student',
            '-score',
        ]

    def __str__(self):
        return str(self.score)

    def get_absolute_url(self):
        return reverse(
            "teachadmin:lessontest_detail",
            kwargs={
                "subject_pk":self.lessonTest.lesson.subject.pk,
                "lesson_pk":self.lessonTest.lesson.pk,
                "pk":self.lessonTest.pk
                }
            )
    
    def clean(self):
        # Don't allow user to enter scores that are lower/higher than LessonTest's min/max scores.
        if self.score > self.lessonTest.max_score:
            raise ValidationError({
                "score": ValidationError(_("Score cannot be higher than the lessontest's maximum score."), code='invalid')
            })
        if self.score < self.lessonTest.min_score:
            raise ValidationError({
                "score": ValidationError(_("Score cannot be lower than the lessontest's minimum score."), code='invalid')
            })
        if self.lessonTest.has_score():
            student_scores = self.lessonTest.scores().filter(student=self.student).select_related('student')
            if student_scores.count() > 0:
                for score in student_scores:
                    if score.score >= self.score:
                        raise ValidationError({
                            "score": ValidationError(_("{} already has a higher score: {} > {}".format(
                                score.student, score.score, self.score
                            )), code='invalid')
                        })
        

class BehaviorType(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)

    class Meta:
        ordering = [
            'name',
            'teacher'
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("teachadmin:behaviortype_detail", kwargs={"pk": self.pk})
    

class BehaviorEvent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    behaviorType = models.ForeignKey(BehaviorType, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    comment = models.TextField(max_length=300)

    class Meta:
        ordering = [
            'timestamp',
            'behaviorType',
            'student'
        ]

    def __str__(self):
        return "{}: {}".format(
            self.behaviorType,
            self.student
        )
    
    def get_absolute_url(self):
        return reverse("teachadmin:behaviorevent_detail", kwargs={"pk": self.pk})
    

class Homework(models.Model):
    name = models.CharField(max_length=50, help_text="Within 50 characters.")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    min_score = models.PositiveSmallIntegerField(default=0, help_text="Default: 0")
    max_score = models.PositiveSmallIntegerField(default=100, help_text="Default: 100")
    deadline = models.DateTimeField(default=timezone.now, help_text="Format: YYYY-MM-DD HH:MM:SS")

    class Meta:
        ordering = [
            'deadline',
            'name',
            'lesson',
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("teachadmin:homework_detail", kwargs={
            "subject_pk": self.lesson.subject.pk,
            "lesson_pk":self.lesson.pk,
            "pk": self.pk
        })

    def has_score(self):
        return self.homeworkscore_set.all().exists()
    
    def students(self):
        """ Returns a list of UNIQUE students that has scores for the current homework. """

        if self.has_score():
            students = []
            scores = self.homeworkscore_set.all()
            for score in scores:
                if score.student not in students:
                    students.append(score.student)
            return students
        else:
            return False
    
    def scores(self):
        return self.homeworkscore_set.all().select_related('student')


class HomeworkScore(models.Model):
    score = models.PositiveSmallIntegerField()
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    turn_in_time = models.DateTimeField(
        default=timezone.now,
        help_text="Format: YYYY-MM-DD HH:MM:SS"
    )

    class Meta:
        ordering = [
            'homework',
            'student',
            'score',
        ]

    def __str__(self):
        return str(self.score)

    def get_absolute_url(self):
        return reverse("teachadmin:homework_detail",
                        kwargs={
                            "subject_pk": self.homework.lesson.subject.pk,
                            "lesson_pk": self.homework.lesson.pk,
                            "pk": self.homework.pk
                            })

    def clean(self):
        # Don't allow for scores higher than the homework's max_score field
        if self.score > self.homework.max_score:
            raise ValidationError({
                "score": ValidationError(_("Score cannot be higher than the homework's maximum score."), code='invalid')
            })
        if self.score < self.homework.min_score:
            raise ValidationError({
                "score": ValidationError(_("Score cannot be lower than the homework's minimum score."), code='invalid')
            })
        if self.homework.has_score():
            student_scores = self.homework.scores().filter(student=self.student).select_related('student')
            if student_scores.exists():
                for score in student_scores:
                    if score.score > self.score:
                        raise ValidationError({
                            "score": ValidationError(_("{} already has a higher score for this homework: {} > {}".format(
                                score.student, score.score, self.score
                            )), code='invalid')
                        })
        if self.turn_in_date > timezone.now():
            ValidationError(_("Did the future {} turn in the paper? I don't think it works that way.".format(self.student)),
                code='invalid'
            )

        

    
