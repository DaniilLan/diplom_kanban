from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Group, UsersGroup


@receiver(post_save, sender=User)
def add_user_to_existing_group(sender, instance, created, **kwargs):
    if created:
        target_group = Group.objects.get(name="GeneralGroup")

        # Добавить пользователя в группу
        UsersGroup.objects.get_or_create(
            group=target_group,
            user=instance
        )