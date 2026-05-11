from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from reviews.models import Review, Comment
from reviews.serializers import ReviewSerializer, CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save(
            author=self.request.user.id,  # временно
            title_id=title_id
        )

    def perform_update(self, serializer):
        if self.request.user.id != serializer.instance.author:
            if not self.request.user.is_staff:
                raise PermissionDenied('Нельзя редактировать чужой отзыв')
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.id != instance.author:
            if not self.request.user.is_staff:
                raise PermissionDenied('Нельзя удалять чужой отзыв')
        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Comment.objects.filter(review_id=review_id)

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        serializer.save(
            author=self.request.user.id,  # временно
            review_id=review_id
        )

    def perform_update(self, serializer):
        if self.request.user.id != serializer.instance.author:
            if not self.request.user.is_staff:
                raise PermissionDenied('Нельзя редактировать чужой комментарий')
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.id != instance.author:
            if not self.request.user.is_staff:
                raise PermissionDenied('Нельзя удалять чужой комментарий')
        instance.delete()
