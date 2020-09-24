from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional Info
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='teachers/profile_pics/', blank=True)
    country = CountryField(blank=True, blank_label='(Select country)')

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("teacher_detail", kwargs={"pk": self.pk})

    def has_homeroom(self):
        if self.homeroom_set.all().count() == 0:
            return False
        else:
            return True
    

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
        return reverse("teachadmin:homeroom_detail", kwargs={"pk": self.pk})

    def has_students(self):
        if self.student_set.all().count() >= 1:
            return True
        return False

    def has_subject(self):
        if self.subject_set.all().count() >= 1:
            return True
        return False
    

class Subject(models.Model):
    name = models.CharField(max_length=50, help_text="Anything within 50 characters.")
    teacher = models.ManyToManyField(Teacher)
    school = models.ForeignKey(School, blank=True, null=True, on_delete=models.CASCADE)
    homeroom = models.ManyToManyField(HomeRoom)

    class Meta:
        ordering = [
            'name',
            'school'
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("teachadmin:subject_detail", kwargs={"pk": self.pk})

    def has_exam(self):
        if self.exam_set.all().count() == 0:
            return False
        else:
            return True
    
    def has_assignment(self):
        if self.assignment_set.all().count() == 0:
            return False
        else:
            return True
    
    def has_lesson(self):
        if self.lesson_set.all().count() == 0:
            return False
        else:
            return True


class Exam(models.Model):
    name = models.CharField(max_length=100, help_text="Anything within 100 characters.")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    
    max_score = models.PositiveSmallIntegerField(default=100, help_text="Default: 100")
    min_score = models.PositiveSmallIntegerField(default=0, help_text="Default: 0")
    date = models.DateField(blank=True)

    class Meta:
        ordering = [
            'subject',
            'date',
            'name'
        ]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("teachadmin:exam_detail", kwargs={
            "subject_pk": self.subject.pk,
            "pk": self.pk
            })

    def has_score(self):
        if self.examscore_set.all().count() == 0:
            return False
        else:
            return True


class Lesson(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name="Start date", null=True)
    end_date = models.DateField(verbose_name="End date", null=True)

    class Meta:
        ordering = [
            'start_date',
            'name'
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("teachadmin:lesson_detail", kwargs={
            "pk": self.pk,
            "subject_pk": self.subject.pk
            })

    def has_lessontest(self):
        if self.lessontest_set.all().count() >= 1:
            return True
        return False
    
    def has_homework(self):
        if self.homework_set.all().count() >= 1:
            return True
        return False


class LessonTest(models.Model):
    name = models.CharField(max_length=50, help_text="Within 50 characters.")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    max_score = models.PositiveSmallIntegerField(default=100, help_text="Default: 100")
    min_score = models.PositiveSmallIntegerField(default=0, help_text="Default: 0")
    test_date = models.DateField(blank=True, help_text="Format: yyyy-mm-dd")

    class Meta:
        ordering = [
            'lesson',
            'test_date',
            'name'
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

    def has_score(self):
        """ Checks whether the LessonTest has any test scores associated with it.
            INPUT: None
            OUTPUT: bool """

        if self.lessontestscore_set.all().count() > 0:
            return True
        return False
    
    def students(self):
        """ Returns UNIQUE students that has scores for the current test. """

        if self.has_score():
            return self.lesson.subject.student_set.distinct()
        else:
            return False

    def scores(self):
        """ Returns all the scores associated with the current test. """
        if self.has_score():
            return LessonTestScore.objects.filter(lessonTest=self)
        else:
            return False

class Student(models.Model):
    first_name = models.CharField(max_length=50, help_text="Within 50 characters.")
    last_name = models.CharField(
        max_length=50,
        blank=True,
        default="",
        help_text="Within 50 characters.")
    student_number = models.CharField(
        max_length=20,
        blank=True,
        default="",
        help_text="Within 50 characters.")
    homeroom = models.ForeignKey(HomeRoom, blank=True, null=True, on_delete=models.SET_NULL)
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


class Assignment(models.Model):
    name = models.CharField(max_length=50)
    max_score = models.PositiveSmallIntegerField(default=100)
    min_score = models.PositiveSmallIntegerField(default=0)
    deadline = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    creator = models.ManyToManyField(Teacher)

    class Meta:
        ordering = [
            'name',
            'deadline',
            'subject'
        ]

    def get_absolute_url(self):
        return reverse("teachadmin:assignment_detail", kwargs={"subject_pk": self.subject.pk, "pk": self.pk})

    def __str__(self):
        return "{}".format(self.name)

    def has_score(self):
        if self.assignmentscore_set.all.count() == 0:
            return False
        else:
            return True


class AssignmentScore(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()
    turn_in_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['assignment', 'turn_in_date', 'score']

    def __str__(self):
        if self.assignment.min_score == 0 and self.assignment.max_score == 100:
            return "{}".format(self.score)
        else:
            return "{} ({}%)".format(self.score,
                round((self.score/self.assignment.max_score)*100,1))


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
            'student'
        ]

    def __str__(self):
        return "{}".format(self.score)

    def get_absolute_url(self):
        return reverse("teachadmin:exam_detail", kwargs={
            "pk": self.exam.pk,
            "subject_pk": self.exam.subject.pk
            })


class LessonTestScore(models.Model):
    score = models.PositiveSmallIntegerField(default=0)
    lessonTest = models.ForeignKey(LessonTest, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        ordering = [
            'lessonTest',
            'student'
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
    creator = models.ForeignKey(Teacher, null=True, on_delete=models.SET_NULL)
    behaviorType = models.ForeignKey(BehaviorType, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    comment = models.CharField(max_length=100)

    class Meta:
        ordering = [
            'timestamp',
            'student',
            'behaviorType',
            'creator'
        ]

    def __str__(self):
        return "{} #{} {}".format(
            self.behaviorType,
            self.student.student_number,
            self.student.first_name
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
            'lesson',
            'name'
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
        if self.homeworkscore_set.all().count() >= 1:
            return True
        return False


class HomeworkScore(models.Model):
    score = models.PositiveSmallIntegerField()
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        ordering = [
            'student',
            'homework',
            'score'
        ]

    def __str__(self):
        return self.score

    def get_absolute_url(self):
        return reverse("teachadmin:homework_detail",
                        kwargs={
                            "subject_pk": self.homework.lesson.subject.pk,
                            "lesson_pk": self.homework.lesson.pk,
                            "pk": self.homework.pk
                            })

    def clean(self):
        if self.score > self.homework.max_score:
            raise ValidationError(_("Score cannot be higher than the Homework's max score. (%(score)s > %(max_score)s)"),
                                  params={'score': self.score, 'max_score': self.homework.max_score})
            
    

    
