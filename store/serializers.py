from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Book, UserBookRelation

class BookSerializer(ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    annotated_likes = serializers.IntegerField(read_only=True)
    class Meta:
        model = Book
        fields = ('id', 'title', 'price', 'author', 'likes_count', 'annotated_likes')
    def get_likes_count(self, instance):
        return UserBookRelation.objects.filter(book=instance, like=True).count()

class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ("book", "like", "in_bookmarks", "rate")