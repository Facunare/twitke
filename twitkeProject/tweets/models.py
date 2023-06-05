from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

class Tweet(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    content = models.TextField(max_length=180)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    retweets = models.IntegerField(default=0)
    edited = models.BooleanField(default=False)
    responses = models.IntegerField(null=True, default=0)
    

    
    
class TweetImage(models.Model):
    tweet = models.ForeignKey(Tweet, related_name='images', on_delete=models.CASCADE)
    image = models.FileField(null=True, blank=True, upload_to='tweetImages')
    video = models.FileField(null=True, blank=True, upload_to='tweetVideos')
