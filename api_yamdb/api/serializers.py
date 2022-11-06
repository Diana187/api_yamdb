from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, ValidationError

from reviews.models import Title, Category
from users.models import User


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        fields = '__all__'
        model = User

        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['user', 'confirmation_code']
            )
        ]


class SignUpSerializer():
    


class UserSerializer():
    pass


class NotAdminSerializer():
    pass


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


# class TitleSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Title
#         fields = ('id', 'name', 'year', 'category')

