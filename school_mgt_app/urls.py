from django.urls import path
from .views import register_view
from . import views
from school_mgt_app import views

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('director/', views.director_dashboard, name='director_dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('director/dashboard/', views.director_dashboard, name='director_dashboard'),
]