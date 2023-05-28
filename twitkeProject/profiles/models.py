from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tweets.models import Tweet

# Create your models here.

class Profiles(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE )
    username = models.CharField(max_length=30, null=True, default="")
    keeps = models.ManyToManyField(Tweet, related_name='kept_by_profiles', blank=True)
    retweets = models.ManyToManyField(Tweet, related_name='retweets_by_profiles', blank=True)
    biography = models.TextField(max_length=250,  null=True, default="", blank=True)
    profileImage = models.ImageField(null=True, blank=True, upload_to='profileImages')
    profileBanner = models.ImageField(null=True, blank=True, upload_to='profileBanners')
    followers = models.IntegerField(default=0)
    followers_users = models.ManyToManyField('self', symmetrical=False, related_name="followage", blank=True)
    followed_users = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    like_tweets = models.ManyToManyField(Tweet, related_name='liked', blank=True)
    birthday = models.DateField(null=True)
    webSite = models.CharField(null=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    darkMode = models.BooleanField(default=False)
    def __str__(self):
        return self.username

class verfifyRequests(models.Model):
    profile = models.ForeignKey(Profiles, null=True, on_delete=models.CASCADE)
    