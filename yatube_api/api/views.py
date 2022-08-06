
from django.shortcuts import get_object_or_404

from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError

from posts.models import Comment, Follow, Group, Post, User

from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    FolllowSerializer,
    GroupSerializer,
    PostSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    """Получение и изменение публикаций."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Только получение информации о группах."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Получение и изменение комментариев к постам."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


class FolllowViewSet(viewsets.ModelViewSet):
    """Подписка на автора."""
    serializer_class = FolllowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        return user.follower.all()

    def perform_create(self, serializer):
        username = self.request.data.get('following')
        following = get_object_or_404(User, username=username)
        user = self.request.user
        if user == following:
            raise ValidationError('Невозможно подписаться на себя!')
        if Follow.objects.filter(
                user=user,
                following=following).exists():
            raise ValidationError('Уже есть подписка!')
        serializer.save(user=user, following=following)
