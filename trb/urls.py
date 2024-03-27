# urls.py
from django.urls import path, include
from . import views
from .views import StudentProfileCreateView, student_profile_created_view, student_logout, delete_student, deny_student, students_list, student_detail_requests, student_details

urlpatterns = [
    path('', views.home, name='home'),
    path('student/signup/', views.student_signup, name='student_signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('student/login/', views.student_login, name='student_login'),
    path('student/home/', views.student_home, name='student_home'),
    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('teacher/home/', views.teacher_home, name='teacher_home'),
    path('student/profile/create/', StudentProfileCreateView.as_view(), name='student_profile_create'),
    path('student/profile/created/', student_profile_created_view, name='student_profile_created'),
    path('approve-students/', views.approve_student, name='approve_students'),
    path('approve-student/', views.approve_student, name='approve_student'),
    path('delete-student/', views.delete_student, name='delete_student'),
    path('waiting-approval/', views.waiting_approval, name='waiting_approval'),
    path('student/logout/', student_logout, name='student_logout'),
    path('list_student_requests/', views.list_student_requests, name='list_student_requests'),
    path('student/<int:student_id>/deny/', views.deny_student, name='deny_student'),

    path('student/<int:student_id>/', views.student_detail_requests, name='student_detail_requests'),
    path('student/<int:student_id>/approve/', views.approve_student, name='approve_student'),
    path('student/<int:student_id>/delete/', views.delete_student, name='delete_student'),
    path('students-list/', views.students_list, name='students_list'),
    path('students-list/<int:student_id>/', views.student_details, name='student_details'),
    path('student/<int:student_id>/edit/', views.edit_student, name='edit_student'),


    # Add other URLs as needed
]

