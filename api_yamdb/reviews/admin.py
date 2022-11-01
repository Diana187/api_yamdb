from django.contrib import admin

from .models import Reviews, Title, Category, Genre

# ------------------------------------образец класса для отображения в админке
# class ReviewsAdmin(admin.ModelAdmin):
#     list_display = (
#         'pk',
#         'text',
#         'created',
#         'author',
#         'group',
#     )
#     list_editable = ('group',)
#     search_fields = ('text',)
#     list_filter = ('created',)
#     empty_value_display = '-пусто-'


admin.site.register(Reviews)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
