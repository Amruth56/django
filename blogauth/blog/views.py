from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .forms import BlogForm, SignUpForm
from .models import Blog

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('all_blogs')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('my_blogs')
    else:
        form = BlogForm()
    return render(request, 'blog/create_blog.html', {'form': form})

@login_required
def all_blogs(request):
    blogs = Blog.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) | 
            Q(author__username__icontains=search_query)
        )
        
    # Filter by author
    author_filter = request.GET.get('author', '')
    if author_filter:
        blogs = blogs.filter(author__username=author_filter)
        
    # Sort functionality 
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'newest':
        blogs = blogs.order_by('-created_at')
    elif sort_by == 'oldest':
        blogs = blogs.order_by('created_at')
    elif sort_by == 'title':
        blogs = blogs.order_by('title')
    elif sort_by == 'author':
        blogs = blogs.order_by('author__username')
        
    # Date filter
    date_filter = request.GET.get('date_filter', '')
    if date_filter:
        today = datetime.now().date()
        if date_filter == 'today':
            blogs = blogs.filter(created_at__date=today)
        elif date_filter == 'week':
            week_ago = today - timedelta(days=7)
            blogs = blogs.filter(created_at__date__gte=week_ago)
        elif date_filter == 'month':
            month_ago = today - timedelta(days=30)
            blogs = blogs.filter(created_at__date__gte=month_ago)
        
    # Get all authors for filter dropdown
    authors = User.objects.filter(blog__isnull=False).distinct()
    
    context = {
        'blogs': blogs,
        'search_query': search_query,
        'author_filter': author_filter,
        'authors': authors,
        'sort_by': sort_by,
        'date_filter': date_filter,
    } 
    
    return render(request, 'blog/all_blogs.html', context)

@login_required
def my_blogs(request):
    blogs = Blog.objects.filter(author=request.user)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) 
        )
        
    # Sort functionality 
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'newest':
        blogs = blogs.order_by('-created_at')
    elif sort_by == 'oldest':
        blogs = blogs.order_by('created_at')
    elif sort_by == 'title':
        blogs = blogs.order_by('title')
        
    # Date filter
    date_filter = request.GET.get('date_filter', '')
    if date_filter:
        today = datetime.now().date()
        if date_filter == 'today':
            blogs = blogs.filter(created_at__date=today)
        elif date_filter == 'week':
            week_ago = today - timedelta(days=7)
            blogs = blogs.filter(created_at__date__gte=week_ago)
        elif date_filter == 'month':
            month_ago = today - timedelta(days=30)
            blogs = blogs.filter(created_at__date__gte=month_ago)
            
    context = {
        'blogs': blogs,
        'search_query': search_query,
        'sort_by': sort_by,
        'date_filter': date_filter,
    }
    return render(request, 'blog/my_blogs.html', context)

@login_required
def edit_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('my_blogs')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blog/edit_blog.html', {'form': form})

@login_required
def delete_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    blog.delete()
    return redirect('my_blogs')
