from django.shortcuts import render, redirect
from .models import BlogPost
from .forms import BlogForm

# Create your views here.

def index(request):
    """Home page displaying Blog Posts"""
    titles = BlogPost.objects.order_by('-date_added')
    context = {'titles':titles}
    return render(request, 'BlogPost/index.html', context)

def new_blog(request):
    """Add a new blog post"""
    if request.method != 'POST':
        form = BlogForm()
    else:
        form = BlogForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('BlogPost:index')

    context = {'form':form}
    return render(request, 'BlogPost/new_blog.html', context)

def edit_blog(request, blog_id):
    blog = BlogPost.objects.get(id=blog_id)

    if request.method != 'POST':
        form = BlogForm(instance=blog)
    else:
        form = BlogForm(instance=blog, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('BlogPost:index')
    
    context = {'blog':blog, 'form':form}
    render(request, 'BlogPost/edit_blog.html', context)



    
