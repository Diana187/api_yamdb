from django.conf import settings
#from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField('Категория', max_length=50)
    slug = models.SlugField('Слаг', default='слаг не указан', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=50)
    slug = models.SlugField('Слаг', default='слаг не указан')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Наименование произведения', max_length=200)
    year = models.CharField('Год создания произведения', max_length=4)
    category = models.ForeignKey(
        Category,
        verbose_name='категория',
        on_delete=models.CASCADE,
        related_name='titles',
        help_text='название категории',
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='жанр',
        help_text='наименование жанра',
        related_name='titles',
    )
    description = models.CharField(
        'Описание произведения',
        max_length=250,
        default='нет описания'
    )

    rating = models.PositiveSmallIntegerField(
        'Рейтинг произведения',
        default=0
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField(
        'Текст отзыва',
        help_text='Введите текст отзыва'
    )

    score = models.CharField(
        'Рейтинг',
        max_length=2,
        choices=settings.SCORE_CHOICES,
        null=True
    )

    pub_date = models.DateTimeField(
        'Дата создания отзыва',
        auto_now_add=True,
        db_index=True,
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text='название произведения'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text='Имя автора отзыва',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:settings.FIRST_SYMBOLS]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments',
        help_text='ID отзыва',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments',
        help_text='ID автора',
    )
    text = models.TextField(
        'Текст комментария',
        help_text='Введите текст комментария'
    )
    pub_date = models.DateTimeField(
        'Дата создания комментария',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:settings.FIRST_SYMBOLS]
