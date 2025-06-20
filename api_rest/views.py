# core/views.py

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Document
from .serializers import UserSerializer, DocumentSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.get_or_create(user=user)
        
class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Credenciais inválidas'}, status=400)

class DocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return Document.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return Document.objects.all()
    
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

class DocumentSaveView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        document = get_object_or_404(Document, pk=pk)
        content = request.data.get("content")
        title = request.data.get("title")
        plain_text = request.data.get("plain_text")

        if content is not None:
            document.content = content

        if title is not None:
            document.title = title
            
        if plain_text is not None:
            document.plain_text = plain_text

        document.save()

        return Response({
            "success": True,
            "document": {
                "id": document.id,
                "title": document.title,
                "content": document.content,
                "plain_text": document.plain_text
            }
        }, status=status.HTTP_200_OK)