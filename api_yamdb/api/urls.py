from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, TitleViewSet, GenresViewSet, ReviewViewSet

router = routers.SimpleRouter()
router.register('categories', CategoryViewSet)
router.register('titles', TitleViewSet)
router.register('genres', GenresViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename=r'v1/titles/(?P<title_id>\d+)/reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/',
    ReviewViewSet,
    basename=(
        r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/'
    )
)

urlpatterns = [
    path('v1/', include(router.urls)),

]
