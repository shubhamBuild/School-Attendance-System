from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='login.html'
        ),
        name='login'
    ),

    path('', views.dashboard, name='dashboard'),

    path('mark/', views.mark_attendance, name='mark_attendance'),

    path('records/', views.attendance_list, name='attendance_list'),

]