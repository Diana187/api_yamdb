# Generated by Django 3.2.9 on 2022-11-01 19:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Категория')),
                ('slug', models.SlugField(default='категория не выбрана', verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Жанр')),
                ('slug', models.SlugField(default='жанр не выбран', verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование произведения')),
                ('year', models.IntegerField(verbose_name='Год создания произведения')),
                ('category', models.ForeignKey(help_text='название категории', on_delete=django.db.models.deletion.CASCADE, related_name='titles', to='reviews.category', verbose_name='категория')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Введите текст отзыва', verbose_name='Текст отзыва')),
                ('score', models.IntegerField(verbose_name='Рейтинг')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания отзыва')),
                ('author', models.ForeignKey(help_text='Имя автора отзыва', on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Автор отзыва')),
                ('title', models.ForeignKey(help_text='название произведения', on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.title', verbose_name='Произведение')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='GenreTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(help_text='наименование жанра', on_delete=django.db.models.deletion.CASCADE, related_name='genres', to='reviews.genre', verbose_name='жанр')),
                ('title', models.ForeignKey(help_text='наименование произведения', on_delete=django.db.models.deletion.CASCADE, related_name='genres', to='reviews.title', verbose_name='произведение')),
            ],
            options={
                'verbose_name': 'Жанры-Произведения',
                'verbose_name_plural': 'Жанры-Произведения',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Введите текст комментария', verbose_name='Текст комментария')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания комментария')),
                ('author', models.ForeignKey(help_text='ID автора', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария')),
                ('review', models.ForeignKey(help_text='ID отзыва', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.review', verbose_name='Отзыв')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('-pub_date',),
            },
        ),
    ]