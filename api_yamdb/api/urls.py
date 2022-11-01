from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from api.views import CategoryViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)

# router.register(r'posts/(?P<post_id>\d+)/comments',
#                 CommentViewSet,
#                 basename=r'v1/posts/(?P<post_id>\d+)/comments')

urlpatterns = [
    path('v1/', include(router.urls)),

]
