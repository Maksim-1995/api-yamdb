from rest_framework import serializers
from .models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'score', 'pub_date', 'author')
        read_only_fields = ('pub_date',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'review', 'text', 'pub_date', 'author')
        read_only_fields = ('pub_date',)
