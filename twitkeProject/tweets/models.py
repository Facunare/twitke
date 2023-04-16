from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.

class Tweet(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    content = models.TextField(max_length=180)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    likes_users = models.ManyToManyField(User, related_name="likes_tweets")
    retweets = models.IntegerField(default=0)
    parent_tweet = models.IntegerField(null=True)
    
    