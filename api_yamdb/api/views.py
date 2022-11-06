import codecs
import csv

from django.core.mail import EmailMessage
from rest_framework import (permissions, response,
                            generics, status)
# from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import (ObjectReadOnly, AuthorOrReadOnly,
                             AdminOnly, AdminOrReadOnly)
from .serializers import (CategorySerializer, SignUpSerializer,
                          GetTokenSerializer)
from api.mixins import ListCreateDestroyViewSet
from reviews.models import Category
from users.models import User


class APIToken(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class APISignup(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email_body = (
            f'Доброе дкень, {user.username}!'
            f'\nВаш код подтверждения: {user.confirmation_code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Ваш подтверждения доступа к API'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    pass
    


class UserCreateViewSet(generics.CreateAPIView):
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

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
