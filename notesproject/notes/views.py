from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Notes  # Changed from Note to Notes
from .serializers import NotesSerializer
from .permissions import IsOwner


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NotesSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return Notes.objects.filter(owner=self.request.user)  # Changed from Note to Notes
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)
        
    def perform_destroy(self, instance):
        instance.delete()