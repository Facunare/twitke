from django.db import models
from tweets.models import Tweet
from profiles.models import Profiles
# Create your models here.

class Tweet_profile(models.Model):
    tweet = models.ForeignKey(Tweet, null=True, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profiles, null=True, on_delete=models.CASCADE)
    