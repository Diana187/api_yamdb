from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, TitleViewSet

router = routers.SimpleRouter()
router.register('categories', CategoryViewSet)
router.register('titles', TitleViewSet)

# router.register(r'posts/(?P<post_id>\d+)/comments',
#                 CommentViewSet,
#                 basename=r'v1/posts/(?P<post_id>\d+)/comments')

urlpatterns = [
    path('v1/', include(router.urls)),

]
