from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .models import Blog
from .serializers import BlogSerializer, BlogListSerializer

class BlogListAPIView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating blogs
    GET: List all blogs with filtering and search
    POST: Create a new blog
    """
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Blog.objects.all()
        
        # Search functionality
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(author__username__icontains=search_query)
            )
        
        # Filter by author
        author_filter = self.request.query_params.get('author', None)
        if author_filter:
            queryset = queryset.filter(author__username=author_filter)
        
        # Sort functionality
        sort_by = self.request.query_params.get('sort', 'newest')
        if sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'oldest':
            queryset = queryset.order_by('created_at')
        elif sort_by == 'title':
            queryset = queryset.order_by('title')
        elif sort_by == 'author':
            queryset = queryset.order_by('author__username')
        
        # Date filter
        date_filter = self.request.query_params.get('date_filter', None)
        if date_filter:
            today = datetime.now().date()
            if date_filter == 'today':
                queryset = queryset.filter(created_at__date=today)
            elif date_filter == 'week':
                week_ago = today - timedelta(days=7)
                queryset = queryset.filter(created_at__date__gte=week_ago)
            elif date_filter == 'month':
                month_ago = today - timedelta(days=30)
                queryset = queryset.filter(created_at__date__gte=month_ago)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BlogDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating and deleting a blog
    GET: Get blog details
    PUT/PATCH: Update blog
    DELETE: Delete blog
    """
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Blog.objects.all()

class MyBlogsAPIView(generics.ListAPIView):
    """
    API endpoint for listing current user's blogs
    GET: List current user's blogs with filtering
    """
    serializer_class = BlogListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Blog.objects.filter(author=self.request.user)
        
        # Search functionality
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        
        # Sort functionality
        sort_by = self.request.query_params.get('sort', 'newest')
        if sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'oldest':
            queryset = queryset.order_by('created_at')
        elif sort_by == 'title':
            queryset = queryset.order_by('title')
        
        # Date filter
        date_filter = self.request.query_params.get('date_filter', None)
        if date_filter:
            today = datetime.now().date()
            if date_filter == 'today':
                queryset = queryset.filter(created_at__date=today)
            elif date_filter == 'week':
                week_ago = today - timedelta(days=7)
                queryset = queryset.filter(created_at__date__gte=week_ago)
            elif date_filter == 'month':
                month_ago = today - timedelta(days=30)
                queryset = queryset.filter(created_at__date__gte=month_ago)
        
        return queryset

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def authors_list(request):
    """
    API endpoint for listing all authors
    GET: List all users who have written blogs
    """
    authors = User.objects.filter(blog__isnull=False).distinct()
    data = [
        {
            'id': author.id,
            'username': author.username,
            'email': author.email,
            'first_name': author.first_name,
            'last_name': author.last_name,
            'blog_count': author.blog_set.count()
        }
        for author in authors
    ]
    return Response(data)

@api_view(['GET'])
def api_info(request):
    """
    API endpoint for API documentation and info
    GET: Get API information and available endpoints
    """
    info = {
        'api_name': 'BlogAuth API',
        'version': '1.0',
        'description': 'REST API for blog management with authentication',
        'endpoints': {
            'blogs': {
                'list': '/api/blogs/',
                'detail': '/api/blogs/{id}/',
                'my_blogs': '/api/blogs/my/',
                'authors': '/api/authors/',
            },
            'authentication': {
                'login': '/api/auth/login/',
                'logout': '/api/auth/logout/',
                'register': '/api/auth/register/',
            }
        },
        'query_parameters': {
            'search': 'Search blogs by title, content, or author',
            'author': 'Filter blogs by author username',
            'sort': 'Sort blogs (newest, oldest, title, author)',
            'date_filter': 'Filter by date (today, week, month)',
            'page': 'Page number for pagination',
        }
    }
    return Response(info) 