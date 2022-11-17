import uuid

from django.core.mail import EmailMessage
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import AnonReadOnly, IsAdmin
from users.models import User
from users.serializers import (TokenSerializer, SignupSerializer,
                               UserSerializer, ForUserSerializer)


class APITokenView(generics.CreateAPIView):
    permission_classes = (AnonReadOnly,)
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                f'Пользователь {data["username"]} не зарегистрирован.',
                status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=data['username'])

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

        if request.user.is_admin or request.user.is_superuser:
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )

        elif request.user.is_user or request.user.is_moderator:
            serializer = ForUserSerializer(
                request.user, data=request.data, partial=True
            )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
