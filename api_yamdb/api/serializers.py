from rest_framework import serializers


from reviews.models import Title, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


# class TitleSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Title
#         fields = ('id', 'name', 'year', 'category')

