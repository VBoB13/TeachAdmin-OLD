from django.urls import path

from . import views

app_name = 'teachadmin'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('register/', views.register, name='register'),
    path('logout/', views.teachadmin_logout, name='logout'),
    path('login/', views.teachadmin_login, name='login'),
    path('addSchool/', views.addSchool, name='addSchool'),
    path('homeroom/', views.HomeRoomListView.as_view(), name='homeroom_list'),
    path('homeroom/new/', views.HomeRoomCreateView.as_view(), name='homeroom_new'),
    path('homeroom/<int:pk>/', views.HomeRoomDetailView.as_view(), name='homeroom_detail'),
    path('homeroom/<int:pk>/delete/', views.HomeRoomDeleteView.as_view(), name='homeroom_delete'),
    path('homeroom/<int:pk>/update/', views.HomeRoomUpdateView.as_view(), name='homeroom_update'),
    path('other-students/', views.OtherStudentsList.as_view(), name='other_students_list'),
    path('schools/', views.SchoolListView.as_view(), name='school_list'),
    path('schools/new/', views.SchoolCreateView.as_view(), name='new_school'),
    path('schools/<int:pk>/', views.SchoolDetailView.as_view(), name='school_detail'),
    path('schools/<int:pk>/delete/', views.SchoolDeleteView.as_view(), name='school_delete'),
    path('schools/<int:school_pk>/homerooms/new/', views.HomeRoomCreateView.as_view(), name='school_add_homeroom'),
    path('student/all/', views.StudentListView.as_view(), name='student_list'),
    path('student/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('student/new/', views.StudentCreateView.as_view(), name='student_new'),
    path('student_group/<int:student_class_id>/', views.StudentView.as_view(), name='studentsView'),
    path('student_group/<int:student_class_id>/<int:pk>/', views.StudentDetailView.as_view(), name='studentDetail'),
    path('student_group/add_student/<int:student_group_id>/', views.addStudent, name='addStudent'),
    path('student_group/addTest/<int:student_class_id>/', views.addTest, name='addTest'),
    path('student_group/addAssignment/<int:student_class_id>/', views.addAssignment, name='addAssignment'),
    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('subjects/new/', views.SubjectCreateView.as_view(), name='subject_new'),
    path('subjects/delete/<int:pk>/', views.SubjectDeleteView.as_view(), name='subject_delete'),
    path('subjects/new/<int:student_pk>/', views.SubjectCreateView.as_view(), name='subject_new_student'),
    path('subjects/<int:pk>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('subjects/<int:pk>/add-student/', views.SubjectUpdateView.as_view(), name='subject_add_student'),
    path('subjects/<int:subject_pk>/add-exam/', views.ExamCreateView.as_view(), name='subject_add_exam'),
    path('subjects/<int:subject_pk>/exams/', views.ExamListView.as_view(), name='exam_list'),
    path('subjects/<int:subject_pk>/exams/<int:pk>/', views.ExamDetailView.as_view(), name='exam_detail'),
    path('subjects/<int:subject_pk>/exams/<int:exam_pk>/scores/new/', views.ExamScoreCreateView.as_view(), name='subject_exam_add_score'),
    path('subjects/<int:subject_pk>/exams/<int:exam_pk>/scores/<int:pk>/', views.ExamScoreDetailView.as_view(), name='examscore_detail'),
    path('subjects/<int:subject_pk>/add-lesson/', views.LessonCreateView.as_view(), name='subject_add_lesson'),
    path('subjects/<int:subject_pk>/lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('subjects/<int:subject_pk>/lessons/<int:lesson_pk>/homework/new/', views.HomeworkCreateView.as_view(), name='lesson_add_homework'),
    path('subjects/<int:subject_pk>/lessons/<int:lesson_pk>/homework/<int:pk>/', views.HomeworkDetailView.as_view(), name='homework_detail'),
    path('subjects/<int:subject_pk>/lessons/<int:lesson_pk>/homework/<int:homework_pk>/add-score/', views.HomeworkScoreCreateView.as_view(), name='homework_add_score'),
    path('subjects/<int:subject_pk>/lessons/<int:lesson_pk>/tests/new/', views.LessonTestCreateView.as_view(), name='lesson_add_test'),
    path('subjects/<int:subject_pk>/lessons/<int:lesson_pk>/tests/<int:pk>/', views.LessonTestDetailView.as_view(), name='lessontest_detail'),
    path('subjects/<int:subject_pk>/lessons/<int:lesson_pk>/tests/<int:lessontest_pk>/testscores/new/', views.LessonTestScoreCreateView.as_view(), name='lessontest_add_score'),
    path('subjects/<int:subject_pk>/assignments/<int:pk>/', views.AssignmentDetailView.as_view(), name='assignment_detail'),
    path('subjects/<int:subject_pk>/assignments/new/', views.AssignmentCreateView.as_view(), name='subject_add_assignment'),
    path('subjects/<int:subject_pk>/assignments/delete/<int:pk>/', views.AssignmentDeleteView.as_view(), name='assignment_delete'),
    path('teacher/<int:pk>/', views.TeacherDetailView.as_view(), name='teacher'),
]
