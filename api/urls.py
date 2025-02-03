from api.views import DetailTask, ListTask, TimeLogList

from django.urls import path

urlpatterns = [
    path('tasks/', ListTask.as_view()),
    path('task/<str:pk>', DetailTask.as_view()),
    path('api/timelogs/<int:task_id>/', TimeLogList.as_view(), name='timelog-list'),
]
