from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('student/dashboard/', views.user_dashboard, {'user_type': 'student'}, name='student_dashboard'),
    path('professor/dashboard/', views.user_dashboard, {'user_type': 'professor'}, name='professor_dashboard'),

    # Student Routes
    path('student/signup/', views.student_signup, name='student_signup'),
    path('student/signin/', views.student_signin, name='student_signin'),
path('feedback_success/', views.feedback_success, name='feedback_success'),
    # Professor Routes
    path('professor/signup/', views.professor_signup, name='professor_signup'),
    path('professor/signin/', views.professor_signin, name='professor_signin'),
    path('professor/home/', views.professor_home, name='professor_home'),
    # SignOut
    path('signout/', views.signout, name='signout'),
]
