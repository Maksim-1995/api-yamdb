from django.db import models


class Review(models.Model):
    """Модель отзыва на произведение"""
    title = models.IntegerField(verbose_name='ID произведения')  # временная заглушка
    author = models.IntegerField(verbose_name='Автор')
    text = models.TextField(verbose_name='Текст отзыва')
    score = models.IntegerField(verbose_name='Оценка', help_text='Оценка от 1 до 10')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв на произведение {self.title} от автора {self.author}'


class Comment(models.Model):
    """Модель комментария к отзыву"""
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments', verbose_name='Отзыв')
    author = models.IntegerField(verbose_name='Автор')
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий к отзыву {self.review.id} от автора {self.author}'
