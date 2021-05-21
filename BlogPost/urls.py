from django.urls import path
from . import views

app_name = 'BlogPost'

urlpatterns = [
    path('', views.BlogList.as_view(), name='index'),

    path('user/<str:username>/', views.UserBlogList.as_view(), name='user_posts'),
    
    path('blog/<int:pk>/', views.BlogDetail.as_view(), name='blog_detail'),
    
    path('new_blog/', views.BlogCreate.as_view(), name='new_blog'),
    
    path('blog/<int:pk>/update/', views.BlogUpdate.as_view(), name='blog_update'),

    path('blog/<int:pk>/delete', views.BlogDelete.as_view(), name='blog_delete'),
]
