import uuid

from django.core.mail import EmailMessage
from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin
from django.shortcuts import get_object_or_404
from rest_framework import (filters, generics,
                            status, viewsets, mixins)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import (AnonReadOnly, AuthorOrReadOnly, 
                             AdminOrReaOnly, AdminModeratorAuthorOrReadOnly)
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.pagination import LimitOffsetPagination
from api.serializers import (CategorySerializer, SignupSerializer,
                             TokenSerializer, UserSerializer,
                             NotAdminSerializer, CommentSerializer,
                             GenreSerializer, TitleSerializer,
                             ReviewSerializer)
from reviews.models import Category, Review, Title, Genre, Comment
from users.models import User


class APITokenView(generics.CreateAPIView):
    permission_classes = (AnonReadOnly,)
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        # print(request.data)
        # print(User.objects.filter(username=request.data['username'], 
        #     confirmation_code=request.data['confirmation_code']).one())
        # raise
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                f'Такого пользователя {data["username"]} не зарегистрировано(',
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Этот код подтверждения не подходит('},
            status=status.HTTP_400_BAD_REQUEST)


class APISignupView(APIView):
    permission_classes = (AnonReadOnly,)
    serializer_class = SignupSerializer

    def send_email(self, data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(confirmation_code=str(uuid.uuid4()))
        email_body = (
            f'Добрый день, {user.username}!'
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
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AuthorOrReadOnly,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(AuthorOrReadOnly, IsAuthenticated),
        url_path='me')
    def get_user_info(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UserSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReaOnly, )
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReaOnly, )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminOrReaOnly,)

    # def get_serializer_class(self):
    #     if self.request.method in ('POST', 'PATCH',):
    #         return TitleSerializerDetail
    #     return TitleSerializerList


class ReviewViewSet(UpdateModelMixin, GenericViewSet):
    permission_classes = [AnonReadOnly, ]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'title'
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

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
