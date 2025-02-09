from api.views import DetailTask, ListTask, TimeLogList, TimeLogByTask

from django.urls import path

urlpatterns = [
    path('tasks/', ListTask.as_view()),
    path('task/<str:pk>', DetailTask.as_view()),
    path('timelogs/', TimeLogList.as_view(), name='timelogs'),
    path('timelogs/task/<str:task_uuid>/', TimeLogByTask.as_view(), name='timelogs-by-task'),
]
