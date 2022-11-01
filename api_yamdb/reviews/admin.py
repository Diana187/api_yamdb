from django.contrib import admin

from .models import Review, Title, Category, Genre, GenreTitle


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'category',
    )
    search_fields = ('name', 'year')
    list_filter = ('category',)
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'text',
        'author',
        'score',
        'pub_date',
    )
    search_fields = ('title', 'text', 'pub_date',)
    list_filter = ('created', 'score',)
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    search_fields = ('name', 'slug',)
    list_filter = ('name', 'slug',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    search_fields = ('name', 'slug',)
    list_filter = ('name', 'slug',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'review',
        'author',
        'text',
        'pub_date',
    )
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'genre',
        'title',
    )
    empty_value_display = '-пусто-'


admin.site.register(Review)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(GenreTitle)
