from django.urls import include, path
from rest_framework import routers

from users.views import UserViewSet, APISignupView, APITokenView
from .views import (
    CategoryViewSet,
    TitleViewSet,
    GenresViewSet,
    ReviewViewSet,
    CommentViewSet,
)

router = routers.SimpleRouter()
router.register('categories', CategoryViewSet)
router.register('titles', TitleViewSet)
router.register('genres', GenresViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename=r'reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename=r'comments',
)
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', APISignupView.as_view(), name='signup'),
    path('v1/auth/token/', APITokenView.as_view(), name='get_token'),
]
