# Generated by Django 4.1.3 on 2025-02-26 19:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0020_remove_timelog_id_timelog_uuid'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoardGroup',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255, verbose_name='Название группы')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_groups', to=settings.AUTH_USER_MODEL, verbose_name='Владелец группы')),
            ],
            options={
                'verbose_name': 'Группа досок',
                'verbose_name_plural': 'Группы досок',
            },
        ),
        migrations.AddField(
            model_name='task',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='board.boardgroup', verbose_name='Группа'),
        ),
        migrations.CreateModel(
            name='UsersGroup',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Дата присоединения')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='board.boardgroup', verbose_name='Группа')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_memberships', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Участник группы',
                'verbose_name_plural': 'Участники групп',
                'unique_together': {('group', 'user')},
            },
        ),
    ]
