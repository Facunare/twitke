from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tweets.models import Tweet
# Create your models here.

class Profiles(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE )
    username = models.CharField(max_length=30, null=True, default="")
    biography = models.TextField(max_length=250,  null=True, default="", blank=True)
    profileImage = models.ImageField(null=True, blank=True, upload_to='profileImages')
    followers = models.IntegerField(default=0)
    followers_users = models.ManyToManyField('self', related_name="followers_users", blank=True)
    followed_users = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    birthday = models.DateField(null=True, default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
