from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logged_out.html'), name='logout'),

    #path('posts/<int:pk>/', views.user_posts, name='user_posts'),
    #path('posts/<int:pk>/', views.UserBlogList.as_view(), name='user_posts'),
    
    path('profile/', views.profile, name='profile'),

    path('register/', views.register, name='register'),

    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),

    path('password_reset_done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
        name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    
    path('password_reset_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
        name='password_reset_complete'),
    
] 




