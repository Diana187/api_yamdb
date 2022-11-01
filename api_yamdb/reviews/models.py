from django.conf import settings
from django.db import models


class Title(models.Model):
    pass


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='titles',
        help_text='название произведения',
    )
    text = models.TextField(
        'Текст отзыва',
        help_text='Введите текст отзыва'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text='Имя автора отзыва',
    )
    score = models.IntegerField('Рейтинг')
    pub_date = models.DateTimeField(
        'Дата создания отзыва',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:settings.FIRST_SYMBOLS]


class Category(models.Model):
    name = models.CharField('Категория', max_length=50)
    slug = models.SlugField('Слаг', default='категория не выбрана')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=50)
    slug = models.SlugField('Слаг', default='жанр не выбран')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Review,
                             verbose_name='Комментарии',
                             on_delete=models.CASCADE,
                             related_name='comments',
                             help_text='Комментарии',
                             )

    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name='Автор комментария',
                               on_delete=models.CASCADE,
                               related_name='comments',
                               help_text='Имя автора',
                               )
    text = models.TextField('Текст комментария',
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
