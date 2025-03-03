from django.urls import path

from . import views

app_name = 'board'

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register_request, name='register'),
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('api/user/groups/members/', views.get_user_group_members, name='user_group_members'),
    path('api/tasks/<uuid:task_uuid>/members/', views.get_task_group_members, name='task_group_members'),
    path('api/user/groups/', views.get_user_groups, name='user_groups'),
    path('api/tasks/<uuid:task_uuid>/groups/', views.get_task_groups, name='task_groups'),
]
