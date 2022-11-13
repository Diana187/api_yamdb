import datetime
from rest_framework.serializers import Serializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from reviews.models import Title, Category, Review, Comment, Genre
from users.models import User


class ValidateUsernameEmailMixin:
    """Миксин проверки email и корректного имени пользователя."""

    username = serializers.RegexField(
        max_length=50, regex=r'^[\w.@+-]+\Z', required=True
    )
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise ValidationError('Пользователь с таким email уже существует.')

        return value

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(
                'Запрещено использовать "me" в качестве имени пользователя'
            )
        elif User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                f'Данное имя {value} занято, используйте другое...'
            )
        return value


class TokenSerializer(Serializer):
    """Сериализатор для выдачи токена юзеру."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = '__all__'
        model = User


class SignupSerializer(
    serializers.ModelSerializer, ValidateUsernameEmailMixin
):
    """Сериализатор для формы регистрации."""
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'username',
        )


class UserSerializer(serializers.ModelSerializer, ValidateUsernameEmailMixin):
    """Сериализатор для модели User."""
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class ForUserSerializer(UserSerializer):
    """Сериализатор для выдачи роли юзеру."""

    role = serializers.CharField(read_only=True)


class NotAdminSerializer(serializers.ModelSerializer):
    """ Сериализатор для пользователей не являющихся администраторами."""

    class Meta:
        model = User
        fields = ('username', 'email')


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
        source='reviews__score__avg', read_only=True
    )

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

    def validate_year(self, value):
        """
        Нельзя добавлять произведения, которые еще не вышли
        (год выпуска не может быть больше текущего)
        """
        if value > datetime.datetime.now().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего'
            )
        return value
