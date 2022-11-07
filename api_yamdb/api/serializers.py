from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Title, Category, Review, Comment, Genre
from users.models import User


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = '__all__'
        model = User


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    # confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'username',)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Это имя нельзя использовать('
            )
        return username


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')

class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    avg_score = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', '‘avg_score’',
                  'description', 'genre', 'category')

    def get_queryset(self):
        queryset = Title.objects.annotate(
            rating=Avg("reviews__score"))

        return queryset


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
