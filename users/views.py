from BlogPost.models import BlogPost
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import ListView
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.views import (PasswordResetView,
                                       PasswordResetConfirmView)
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def register(request):

    if request.method != 'POST':
        form = UserRegistrationForm()
    else:
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.success(request, 'Your account has been successfully created')
            login(request, new_user)
            return redirect('BlogPost:index')
    
    context = {'form':form}
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    if request.method != 'POST':
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    else:
        u_form = UserUpdateForm(data=request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been successfully updated')
            return redirect('users:profile')
    
    context = {'u_form':u_form, 'p_form':p_form}
    return render(request, 'users/profile.html', context)


class PasswordReset(PasswordResetView):
    email_template_name = 'users/password_reset_email.html'
    template_name = 'users/password_reset.html'
    success_url = reverse_lazy('users:password_reset_done')


class PasswordResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy('users:password_reset_complete')
    template_name = 'users/password_reset_confirm.html'


# User posts view using funciton based views
def user_posts(request,pk):
    post_owner = User.objects.get(id=pk)
    user_posts = post_owner.blogpost_set.all().order_by('-date_added')
    paginator = Paginator(user_posts, 3)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    context = {'post_owner':post_owner, 'page_obj':page_obj}
    return render(request, 'users/user_posts.html', context)


# User posts view using class based views
class UserBlogList(ListView):
    model = User
    template_name = 'users/post.html'
    paginate_by = 3
    context_object_name = 'user_posts'
    
    def get_queryset(self):
        owner = get_object_or_404(User, pk=self.kwargs.get('pk'))
        queryset = BlogPost.objects.filter(owner_id=owner.id).order_by('-date_added')
        return queryset


