from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User 

# Create your models here.
class BlogPost(models.Model):
    """A blog the user is posting."""
    title = models.CharField(max_length=50)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    #def get_absolute_url(self):
    #    return reverse('BlogPost:blog_detail', kwargs={'pk': self.pk})
    