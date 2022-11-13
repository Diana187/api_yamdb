import datetime
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Title, Category, Review, Comment, Genre
from reviews.validators import year_validator


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Category."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('review',)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Review."""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author',)
        model = Review

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data

        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Отзыв к произведению уже написан.'
            )
        return data


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Title (чтение)."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True, default=0
    )
    year = serializers.IntegerField(validators=[year_validator])

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Title (создание)."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    class Meta:
        fields = '__all__'
        model = Title
