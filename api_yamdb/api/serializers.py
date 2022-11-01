from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from api_yamdb.reviews.models import Title, Category


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'category')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')
#
#
# class CommentSerializer(serializers.ModelSerializer):
#     author = SlugRelatedField(slug_field='username', read_only=True)
#
#     class Meta:
#         model = Comment
#         fields = ('id', 'author', 'post', 'text', 'created')
