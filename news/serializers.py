from rest_framework import serializers
from news.models import News


class NewsSerializer(serializers.Serializer):
    _id = serializers.CharField(source="id", read_only=True)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=500)
    image = serializers.CharField(max_length=200)
