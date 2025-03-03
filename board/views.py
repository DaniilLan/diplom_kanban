from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.utils.formats import localize
from django.db.models import Q
from .forms import NewUserForm
from .models import Group, Task
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UsersGroup

@login_required
def home(request):
    user_groups = Group.objects.filter(members__user=request.user)
    tasks = Task.objects.filter(
        Q(owner=request.user) |
        Q(groups__in=user_groups)
    ).distinct()

    all_tasks = []
    for t in tasks:
        # Получаем список групп задачи
        task_groups = t.groups.all()

        t_dict = {
            'uuid': str(t.uuid),
            'name': t.name if t.name is not None else 'Без названия',
            'boardName': t.boardName,
            'date': str(localize(t.date)),
            'task_id': str(t.task_id),
            'description': str(t.description),
            'typeTask': str(t.typeTask),
            'priorityTask': str(t.priorityTask),
            'timeEstimateMinutes': str(t.timeEstimateMinutes),
            'groups': [
                {
                    'uuid': str(g.uuid),
                    'name': g.name
                }
                for g in task_groups
            ],
            'responsible': str(t.responsible),
        }
        all_tasks.append(t_dict)

    all_timelogs = []
    t_timelogs = request.user.timelogs.all()
    for tl in t_timelogs:
        t_dict = {
            "task": str(tl.task.uuid),
            "minutesSpent": tl.minutesSpent,
            "date": tl.date.isoformat(),
            "comment": tl.comment,
            "owner_username": tl.owner.username
        }
        all_timelogs.append(t_dict)
    return render(request, 'index.html', {'tasks': all_tasks, 'timelogs': all_timelogs})

def register_request(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request,
                             'Аккаунт зарегистрирован: '
                             'добро пожаловать на сайт!')
            return redirect('board:login')
        messages.error(request, 'Не удалось зарегистрировать аккаунт. '
                                'Проверьте корректность данных и '
                                'попробуйте еще раз!')
    form = NewUserForm()
    return render(request=request,
                  template_name='register.html',
                  context={'register_form': form})


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request,
                              f'Вы вошли на сайт под ником {username}.')
                return redirect('board:home')
            else:
                messages.error(request, 'Неверные имя и/или пароль.')
        else:
            messages.error(request, 'Неверные имя и/или пароль.')
    form = AuthenticationForm()
    return render(request=request, template_name='login.html',
                  context={'login_form': form})


def logout_request(request):
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта.')
    return redirect('board:login')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_group_members(request):
    user = request.user
    # Получаем все группы пользователя
    user_groups = UsersGroup.objects.filter(user=user).values_list('group', flat=True)
    # Получаем всех участников этих групп
    members = UsersGroup.objects.filter(group__in=user_groups).select_related('user')
    # Собираем уникальные username
    unique_usernames = set(member.user.username for member in members)
    return Response(list(unique_usernames))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task_group_members(request, task_uuid):
    try:
        task = Task.objects.get(uuid=task_uuid)
        # Получаем все группы задачи
        groups = task.groups.all()
        # Получаем всех участников этих групп
        members = UsersGroup.objects.filter(group__in=groups).select_related('user')
        # Собираем уникальные username
        unique_usernames = set(member.user.username for member in members)
        return Response(list(unique_usernames))
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_groups(request):
    user = request.user
    groups = UsersGroup.objects.filter(user=user).select_related('group')
    groups_data = [{
        'uuid': ug.group.uuid,
        'name': ug.group.name
    } for ug in groups]
    return Response(groups_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task_groups(request, task_uuid):
    try:
        task = Task.objects.get(uuid=task_uuid)
        groups = task.groups.all().values('uuid', 'name')
        return Response(groups)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=404)