import uuid

from django.core.mail import EmailMessage
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
)
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status, viewsets
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from api.filters import FilterForTitle
from api.permissions import (
    AdminModeratorAuthorOrReadOnly,
    AnonReadOnly,
    AdminOrReaOnly,
    IsAdmin,
)
from api.serializers import (
    CategorySerializer,
    SignupSerializer,
    TokenSerializer,
    UserSerializer,
    CommentSerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleCreateSerializer,
    ReviewSerializer,
    ForUserSerializer,
)

from reviews.models import Category, Review, Title, Genre
from users.models import User, ADMIN, MODERATOR , USER


class CreateListDestroyViewSet(
    CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet
):

    pass


class APITokenView(generics.CreateAPIView):
    permission_classes = (AnonReadOnly,)
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=data['username'])

        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response(
                {'token': str(token)}, status=status.HTTP_201_CREATED
            )
        return Response(
            {'confirmation_code': 'Этот код подтверждения не подходит('},
            status=status.HTTP_400_BAD_REQUEST,
        )


class APISignupView(APIView):
    permission_classes = (AnonReadOnly,)
    serializer_class = SignupSerializer

    def send_email(self, data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']],
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
            'email_subject': 'Ваш подтверждения доступа к API',
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='me',
    )
    def get_user_info(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'GET':
            serializer = UserSerializer(instance=request.user)
            return Response(serializer.data, status=HTTP_200_OK)

        if request.user.role in (ADMIN, 'superuser'):
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )

        elif request.user.role in (USER, MODERATOR):
            serializer = ForUserSerializer(
                request.user, data=request.data, partial=True
            )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReaOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReaOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """
    Получить список всех объектов. Права доступа: Доступно без токена
    """

    queryset = (Title.objects.all().annotate(Avg('reviews__score'))).order_by(
        'name'
    )
    permission_classes = (AdminOrReaOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterForTitle

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (AdminModeratorAuthorOrReadOnly,)
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        queryset = review.comments.all()

        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
