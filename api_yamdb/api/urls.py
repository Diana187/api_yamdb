from django.urls import include, path
from rest_framework import routers


from .views import CategoryViewSet

router_v1 = routers.DefaultRouter()

router_v1.register('categories', CategoryViewSet)

# router.register(r'posts/(?P<post_id>\d+)/comments',
#                 CommentViewSet,
#                 basename=r'v1/posts/(?P<post_id>\d+)/comments')

djoser_patterns = [
    path('v1/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.authtoken')),
    path('v1/auth/', include('djoser.urls.jwt')),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
] + djoser_patterns
