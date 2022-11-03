from rest_framework import serializers

from rest_framework.relations import SlugRelatedField
from reviews.models import Title, Category, Review, Comment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    """ Сериалайзер для модели Review."""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('author',)
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """ Сериалайзер для модели Comment."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)
