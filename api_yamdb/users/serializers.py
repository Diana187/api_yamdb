from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
        if value in ('me', 'Me'):
            raise ValidationError(
                'Запрещено использовать "me" в качестве имени пользователя'
            )
        elif User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                f'Данное имя {value} занято, используйте другое...'
            )
        return value


class TokenSerializer(serializers.Serializer):
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
