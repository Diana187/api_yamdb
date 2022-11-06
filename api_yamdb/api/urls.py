from django.urls import include, path
from rest_framework import routers

from .views import (APITokenView, CategoryViewSet,
                    APISignupView, UserViewSet,
                    TitleViewSet)

router_v1 = routers.DefaultRouter()

router_v1.register('categories', CategoryViewSet)
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('titles', TitleViewSet)


# router.register(r'posts/(?P<post_id>\d+)/comments',
#                 CommentViewSet,
#                 basename=r'v1/posts/(?P<post_id>\d+)/comments')
# User = get_user_model()

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', APISignupView.as_view(), name='signup'),
    path('v1/auth/token/', APITokenView.as_view(), name='get_token'),
]
