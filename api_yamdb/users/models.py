from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from users.constants import (
    MAX_LENGTH_USERNAME,
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_FIRST_NAME,
    MAX_LENGTH_LAST_NAME,
    MAX_LENGTH_BIO,
    MAX_LENGTH_ROLE
)


class User(AbstractUser):
    """Модель пользователя с дополнительными полями."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN)
    )

    username = models.CharField(
        max_length=MAX_LENGTH_USERNAME,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        verbose_name='Имя пользователя'
    )
    email = models.EmailField(
        max_length=MAX_LENGTH_EMAIL,
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    first_name = models.CharField(
        max_length=MAX_LENGTH_FIRST_NAME,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=MAX_LENGTH_LAST_NAME,
        blank=True,
        verbose_name='Фамилия'
    )
    bio = models.TextField(
        max_length=MAX_LENGTH_BIO,
        blank=True,
        verbose_name='Описание'
    )
    role = models.CharField(
        max_length=MAX_LENGTH_ROLE,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='Роль'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    @property
    def is_admin(self):
        """Пользователь с ролью admin или суперюзер."""
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        """Пользователь с ролью moderator (и не admin)."""
        return self.role == self.MODERATOR
