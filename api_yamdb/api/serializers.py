from rest_framework import serializers


from reviews.models import Title, Category


class GetTokenSerializer():
    pass


class SignUpSerializer():
    pass


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

