# core/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Document

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class DocumentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Document
        fields = ("id", "title", "content", "plain_text", "created_at", "updated_at", "user")
