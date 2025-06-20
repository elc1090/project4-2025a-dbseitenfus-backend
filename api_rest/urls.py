# core/urls.py

from django.urls import path
from .views import RegisterView, UserDetailView, LoginView, DocumentListCreateView, DocumentDetailView, DocumentSaveView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('documents/', DocumentListCreateView.as_view()),
    path('documents/<int:pk>/', DocumentDetailView.as_view()),
    path('documents/<int:pk>/save/', DocumentSaveView.as_view(), name='document-save'),
    path('user/', UserDetailView.as_view(), name='user-detail'), 

]