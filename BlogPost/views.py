from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import BlogPost
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView, 
                                DetailView, 
                                CreateView, 
                                UpdateView,
                                DeleteView)


class BlogList(ListView):
    model = BlogPost
    template_name = 'BlogPost/index.html'
    context_object_name = 'posts'
    ordering = ['-date_added']
    paginate_by = 5

class UserBlogList(ListView):
    model = BlogPost
    template_name = 'BlogPost/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return BlogPost.objects.filter(owner=user).order_by('-date_added')


class BlogDetail(DetailView):
    model = BlogPost
    template_name = 'BlogPost/blog_detail.html'
    context_object_name = 'post'


class BlogCreate(LoginRequiredMixin, CreateView):
    model = BlogPost
    template_name = 'BlogPost/new_blog.html'
    fields = ['title','text']
    success_url = reverse_lazy('BlogPost:index')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class BlogUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    context_object_name = 'post'
    template_name = 'BlogPost/edit_blog.html'
    fields = ['title','text']
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.owner:
            return True
        return False


class BlogDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = 'BlogPost/blog_delete.html'
    context_object_name = 'post'  
    success_url = reverse_lazy('BlogPost:index')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.owner:
            return True
        return False
