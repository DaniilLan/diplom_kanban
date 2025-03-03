from django.contrib import admin
from .models import UsersGroup, Group, Task, TimeLog, DeletedTask


class UsersGroupInline(admin.TabularInline):
    model = UsersGroup
    extra = 1  # Количество пустых форм для добавления новых участников
    verbose_name = "Участник группы"
    verbose_name_plural = "Участники группы"
    autocomplete_fields = ['user']  # Автодополнение для поля пользователя


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'date_created', 'member_count')
    list_filter = ('date_created',)
    search_fields = ('name', 'owner__username')
    inlines = [UsersGroupInline]

    # Автодополнение для поиска пользователей при добавлении
    autocomplete_fields = ['owner']

    def member_count(self, obj):
        return obj.members.count()

    member_count.short_description = "Количество участников"


@admin.register(UsersGroup)
class UsersGroupAdmin(admin.ModelAdmin):
    list_display = ('group', 'user', 'date_joined')
    list_filter = ('group', 'user')
    search_fields = (
        'group__name',
        'user__username',
        'user__first_name',
        'user__last_name'
    )
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined',)
    autocomplete_fields = ['group', 'user']  # Автодополнение для полей

    fieldsets = (
        (None, {
            'fields': ('group', 'user')
        }),
    )


# Остальные модели остаются без изменений
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups',)


@admin.register(TimeLog)
class TimeLogAdmin(admin.ModelAdmin):
    pass


@admin.register(DeletedTask)
class DeletedTaskAdmin(admin.ModelAdmin):
    pass