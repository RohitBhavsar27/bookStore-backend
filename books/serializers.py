from rest_framework import serializers
from books.models import Books  


class BookSerializer(serializers.Serializer):
    _id = serializers.CharField(source="id", read_only=True)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=500)
    category = serializers.CharField(max_length=100)
    trending = serializers.BooleanField()
    coverImage = serializers.CharField(max_length=200)
    oldPrice = serializers.FloatField()
    newPrice = serializers.FloatField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
