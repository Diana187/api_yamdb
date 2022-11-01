import codecs
import csv

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import CategorySerializer
from reviews.models import Category


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, methods=['POST'])
    def upload_data_with_validation(self, request):
        file = request.FILES.get('file')
        reader = csv.DictReader(
            codecs.iterdecode(file, 'utf-8'),
            delimeter=','
        )
        data = list(reader)
        serializer = self.serializer_class(data=data, many=True)
        serializer.is_valid(raise_exception=True)

        data_list = []
        for row in serializer.data:
            data_list.append(
                Category(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
            )
        Category.objects.bulk_create(data_list)
        return Response("Данные успешно загружены в БД.")


# class TitleViewSet(viewsets.ModelViewSet):
#     queryset = Title.objects.all()
#     serializer_class = TitleSerializer
#
#     @action(detail=False, methods=['POST'])
#     def upload_data_with_validation(self, request):
#         file = request.FILES.get('file')
#         reader = csv.DictReader(
#             codecs.iterdecode(file, 'utf-8'),
#             delimeter=','
#         )
#         data = list(reader)
#         serializer = self.serializer_class(data=data, many=True)
#         serializer.is_valid(raise_exception=True)
#
#         titles_list = []
#         for row in serializer.data:
#             titles_list.append(
#                 Title(
#                     id=row['id'],
#                     name=row['name'],
#                     year=row['year'],
#                     category=row['category'],
#                 )
#             )
#         Title.objects.bulk_create(titles_list)
#         return Response("Данные успешно загружены в БД.")
