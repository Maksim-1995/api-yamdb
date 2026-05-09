from django.db import models

from api_yamdb.users.models import User
from .constants import (
    NAME_MAX_LENGTH,
    SLUG_MAX_LENGTH,
    TEXT_LIMIT_FOR_REPR,
)


class Category(models.Model):
    """Категории (типы) произведений."""

    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    slug = models.SlugField('Слаг', max_length=SLUG_MAX_LENGTH, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name[:TEXT_LIMIT_FOR_REPR]


class Genre(models.Model):
    """Жанры произведений."""

    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    slug = models.SlugField('Слаг', max_length=SLUG_MAX_LENGTH, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name[:TEXT_LIMIT_FOR_REPR]


class Title(models.Model):
    """Произведения: фильмы, книги, музыка."""

    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    year = models.PositiveSmallIntegerField('Год выпуска', db_index=True)
    description = models.TextField('Описание', blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанры',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name[:TEXT_LIMIT_FOR_REPR]


class GenreTitle(models.Model):
    """Промежуточная модель для связи Title и Genre."""

    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Связь жанра и произведения'
        verbose_name_plural = 'Связи жанров и произведений'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_title_genre'
            )
        ]
