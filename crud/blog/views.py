from django.shortcuts import render, redirect, get_object_or_404
from .models import Post 
from .forms import PostForm 

#Create and Read 
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {
        'posts': posts
    }) 
    
    
def post_create(request):
    if request.method == 'Post':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


#update 
def post_update(request, pk):
    post = get_object_or_404(Post, pk= pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance = post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form= PostForm(instance= post)
    return render(request, 'blog/post_form.html', {
        'form': form
    })
    
#delete 
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {
        'post': post
    })
