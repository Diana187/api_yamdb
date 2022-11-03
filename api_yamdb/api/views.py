import codecs
import csv

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.mixins import UpdateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet


from .serializers import CategorySerializer, CommentSerializer, \
    ReviewSerializer, TitleSerializer
from reviews.models import Category, Review, Comment, Title


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, methods=['POST'])
    def upload_data_with_validation(self, request):
        """Upload data from CSV, with validation."""
        file = request.FILES.get("file")
        reader = csv.DictReader(codecs.iterdecode(file, "utf-8"), delimiter=",")
        data = list(reader)
        serializer = self.serializer_class(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        category_list = []
        for row in serializer.data:
            category_list.append(
                Category(
                    name=row["name"],
                    slug=row["slug"],
                )
            )
        Category.objects.bulk_create(category_list)
        return Response("Данные успешно загружены в БД.")


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

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

        titles_list = []
        for row in serializer.data:
            titles_list.append(
                Title(
                    name=row['name'],
                    year=row['year'],
                    category=row['category'],
                )
            )
        Title.objects.bulk_create(titles_list)
        return Response("Данные успешно загружены в БД.")


class ReviewView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'title'
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_object(self):
        obj, _ = Review.score.objects.get_or_create(
            user=self.request.user,
            title_id=self.kwargs['title']
            )

        return obj

    def post(self, request):
        review = ReviewSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        queryset = review.comments.all()

        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

