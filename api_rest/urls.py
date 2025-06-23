# core/urls.py

from django.urls import path
from .views import (
    RegisterView,
    UserDetailView,
    LoginView,
    DocumentListCreateView,
    DocumentDetailView,
    DocumentSaveView,
    TextToSpeechView,
    GoogleLoginView
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('google-login/', GoogleLoginView.as_view()),
    path('documents/', DocumentListCreateView.as_view()),
    path('documents/<uuid:pk>/', DocumentDetailView.as_view()),
    path('documents/<uuid:pk>/save/', DocumentSaveView.as_view(), name='document-save'),
    path('user/', UserDetailView.as_view(), name='user-detail'), 
    path('tts/', TextToSpeechView.as_view(), name='tts'),
]