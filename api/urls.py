from api import views
from api.views import DetailTask, ListTask, TimeLogList, TimeLogsByTask, TimeLogCreate, GroupList, GroupDetail

from django.urls import path

urlpatterns = [
    path('tasks/', ListTask.as_view()),
    path('task/<str:pk>', DetailTask.as_view()),
    path('timelogs/task/<str:task_uuid>/', TimeLogsByTask.as_view(), name='timelogs-by-task'),
    path('tasks/<uuid:task_uuid>/timelogs/', TimeLogCreate.as_view(), name='timelog-create'),
    path('groups/', GroupList.as_view(), name='grouplist'),
    path('groups/<uuid:pk>/', GroupDetail.as_view(), name='group-detail'),
]
