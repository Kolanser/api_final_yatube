from django.urls import path, include

from .views import CommentViewSet, FolllowViewSet, GroupViewSet, PostViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')
router.register('groups', GroupViewSet, basename='group')
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
router.register('follow', FolllowViewSet, basename='follow')
urlpatterns = [
    path('v1/', include(router.urls)),
    # path('v1/follow/', FolllowViewSet, name='follow'),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
