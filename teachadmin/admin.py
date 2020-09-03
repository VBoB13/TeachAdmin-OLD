from django.contrib import admin

from .models import (Teacher, School, StudentClass, Student,
                        StudentClassTest, StudentClassTestScore,
                        Assignment, AssignmentScore,
                        HomeRoom, Subject, Exam, ExamScore,
                        Lesson, LessonTest, LessonTestScore,
                        BehaviorType, BehaviorEvent,
                        Homework, HomeworkScore)

# Register your models here.
admin.site.register(School)
admin.site.register(StudentClass)
admin.site.register(Student)
admin.site.register(StudentClassTest)
admin.site.register(StudentClassTestScore)
admin.site.register(Assignment)
admin.site.register(AssignmentScore)

# NEW Models here
admin.site.register(Teacher)
admin.site.register(HomeRoom)
admin.site.register(Subject)
admin.site.register(Exam)
admin.site.register(ExamScore)
admin.site.register(Lesson)
admin.site.register(LessonTest)
admin.site.register(LessonTestScore)
admin.site.register(BehaviorType)
admin.site.register(BehaviorEvent)
admin.site.register(Homework)
admin.site.register(HomeworkScore)
