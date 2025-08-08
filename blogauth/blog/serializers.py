from rest_framework import serializers
from .models import Blog 
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializers):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        
class BlogSerializer(serializers.ModelSerializers):
    author = UserSerializer(read_only = True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        source = 'author',
        write_only = True
    )
    
    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'author', 'author_id']
        read_only_fields = ['created_at']
        
class BlogListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only = True)
    
    class Meta:
        model: Blog
        fields = ['id', 'title', 'author', 'created_at', 'content']
        