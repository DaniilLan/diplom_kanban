from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Group, UsersGroup, Task
from django.contrib.auth.admin import UserAdmin

from django.contrib.admin import AdminSite
AdminSite.site_header = "Управление задачами и группами"
AdminSite.site_title = "Админ-панель"
AdminSite.index_title = "Управление системой"

User = get_user_model()
admin.site.unregister(User)

# Добавим новый Inline для отображения групп пользователя
class UserGroupsInline(admin.TabularInline):
    model = UsersGroup
    extra = 1
    verbose_name = "Участие в группе"
    verbose_name_plural = "Участие в группах"
    autocomplete_fields = ['group']
    fields = ('group', 'date_joined')
    readonly_fields = ('date_joined',)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        # Фильтрация уже добавленных групп
        if obj:
            existing_groups = obj.group_memberships.values_list('group_id', flat=True)
            formset.form.base_fields['group'].queryset = Group.objects.exclude(id__in=existing_groups)
        return formset


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'groups_list')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'group_memberships__group')
    inlines = [UserGroupsInline]

    def groups_list(self, obj):
        return ", ".join([g.group.name for g in obj.group_memberships.all()])
    groups_list.short_description = 'Группы'

class UsersGroupInline(admin.TabularInline):
    model = UsersGroup
    extra = 1
    verbose_name = "Участник группы"
    verbose_name_plural = "Участники группы"
    autocomplete_fields = ['user']

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            # И здесь также исправляем на uuid
            existing_users = obj.members.values_list('user__uuid', flat=True)
            formset.form.base_fields['user'].queryset = User.objects.exclude(uuid__in=existing_users)
        return formset

@admin.register(Group)
class BoardGroupAdmin(admin.ModelAdmin):
    inlines = [UsersGroupInline]
    list_display = ('name', 'owner', 'date_created', 'members_count')
    search_fields = ('name', 'owner__username')
    list_filter = ('date_created',)
    readonly_fields = ('uuid', 'date_created')
    filter_horizontal = ()
    raw_id_fields = ('owner',)

    fieldsets = (
        (None, {
            'fields': ('name', 'owner')
        }),
        ('Системная информация', {
            'fields': ('uuid', 'date_created'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Автоматически устанавливаем владельца при создании"""
        if not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    def members_count(self, obj):
        return obj.members.count()
    members_count.short_description = "Количество участников"

@admin.register(UsersGroup)
class UsersGroupAdmin(admin.ModelAdmin):
    list_display = ('group', 'user', 'date_joined')
    list_filter = ('group__name', 'date_joined')
    search_fields = ('group__name', 'user__username')
    readonly_fields = ('date_joined',)
    autocomplete_fields = ['user', 'group']

# Обновляем админку для Task
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # ... ваши существующие настройки ...
    list_filter = ('group', 'owner', 'boardName')
    raw_id_fields = ('group', 'owner')
    autocomplete_fields = ['group']
