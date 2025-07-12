from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        verbose_name='Группы',
        blank=True,
        related_name='customuser_group_set',  # уникальное имя!
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='Права пользователя',
        blank=True,
        related_name='customuser_permissions_set',  # уникальное имя!
    )

    class Meta:
        """Настройки."""

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        """Строковое представление."""
        return self.username
