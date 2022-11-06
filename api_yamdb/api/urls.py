from django.urls import include, path
from rest_framework import routers, mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth import get_user_model
from djoser.conf import settings
from djoser import signals, utils
from djoser.compat import get_user_email
from users.models import User

from .views import CategoryViewSet

router_v1 = routers.DefaultRouter()

router_v1.register('categories', CategoryViewSet)

# router.register(r'posts/(?P<post_id>\d+)/comments',
#                 CommentViewSet,
#                 basename=r'v1/posts/(?P<post_id>\d+)/comments')
# User = get_user_model()

class CustomUserViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = settings.SERIALIZERS.user
    queryset = User.objects.all()
    permission_classes = settings.PERMISSIONS.user_create
    lookup_field = settings.USER_ID_FIELD
    
    def perform_create(self, serializer):
        user = serializer.save()
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )
        context = {"user": user}
        to = [get_user_email(user)]
        if settings.SEND_ACTIVATION_EMAIL:
            settings.EMAIL.activation(self.request, context).send(to)
        elif settings.SEND_CONFIRMATION_EMAIL:
            settings.EMAIL.confirmation(self.request, context).send(to)

    @action(detail=False, methods=['post'], url_path='signup')
    def signup(self, *args, **kwargs):
        return super().create(*args, **kwargs)


router = routers.DefaultRouter()
router.register("auth", CustomUserViewSet)

djoser_patterns = [
    path('v1/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.authtoken')),
    path('v1/auth/', include('djoser.urls.jwt')),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include(router.urls)),
] + djoser_patterns
