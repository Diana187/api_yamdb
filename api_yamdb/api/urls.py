from django.urls import include, path
from rest_framework import routers

from .views import (APITokenView, CategoryViewSet,
                    APISignupView, UserViewSet,
                    TitleViewSet, GenresViewSet, ReviewViewSet)

router_v1 = routers.SimpleRouter()
router_v1.register('categories', CategoryViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register('genres', GenresViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename=r'v1/titles/(?P<title_id>\d+)/reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/',
    ReviewViewSet,
    basename=(
        r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/'
    )
)
router_v1.register('users', UserViewSet, basename='users')

from .views import (APITokenView, CategoryViewSet,
                    APISignupView, UserViewSet,
                    TitleViewSet)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', APISignupView.as_view(), name='signup'),
    path('v1/auth/token/', APITokenView.as_view(), name='get_token'),
]
