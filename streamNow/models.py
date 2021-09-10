from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import requests

# USERS


# POSTS
class Post(models.Model):
    MEDIA_TYPES = [
        ('movie', 'movie'),
        ('tv', 'tv')

    ]


    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    media_type = models.CharField(default='h', max_length=60, choices=MEDIA_TYPES)
    id_media_type = models.IntegerField(default=0)


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('media_detail', kwargs={'media_type': self.media_type, '_id': self.id_media_type})






