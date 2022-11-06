from rest_framework import serializers


from reviews.models import Title, Category



class SignUpSerializer():
    pass

class GetTokenSerializer():
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

