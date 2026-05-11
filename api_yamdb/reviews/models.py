from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

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


class Review(models.Model):
    """Модель отзыва на произведение"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка', 
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        )
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text[:TEXT_LIMIT_FOR_REPR]


class Comment(models.Model):
    """Модель комментария к отзыву"""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:TEXT_LIMIT_FOR_REPR]
