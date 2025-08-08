from symbol import not_test
from rest_framework import serializers 
from .models import Notes


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'title', 'content', 'created_at']
        
        