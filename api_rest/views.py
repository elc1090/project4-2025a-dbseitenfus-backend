# core/views.py

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Document
from .serializers import UserSerializer, DocumentSerializer
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.cloud import texttospeech
import os

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
        print("DADOS RECEBIDOS:", request.data)
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "name": f"{user.first_name} {user.last_name}"
                }
            })
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

# views.py

from google.oauth2 import service_account
from pathlib import Path
from django.http import HttpResponse

class TextToSpeechView(APIView):
    def post(self, request):
        text = request.data.get('text')
        if not text:
            return Response({"error": "Texto ausente"}, status=status.HTTP_400_BAD_REQUEST)

        BASE_DIR = Path(__file__).resolve().parent.parent  # ou onde está o manage.py

        creds = service_account.Credentials.from_service_account_file(
            str(BASE_DIR / "secrets" / "tts-key.json")
        )
        client = texttospeech.TextToSpeechClient(credentials=creds)

        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="pt-BR",
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        return HttpResponse(response.audio_content, content_type='audio/mpeg')
    
class GoogleLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        name = request.data.get("name", "")
        first_name = name.split(" ")[0] if name else ""
        last_name = " ".join(name.split(" ")[1:]) if name else ""

        if not email:
            return Response({"error": "Email é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        if not user:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=User.objects.make_random_password(),
                first_name=first_name,
                last_name=last_name
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "name": f"{user.first_name} {user.last_name}"
            }
        }, status=status.HTTP_200_OK)