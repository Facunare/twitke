from django.db import models
from tweets.models import Tweet, TweetImage
from profiles.models import Profiles
# Create your models here.

class Tweet_profile(models.Model):
    tweet = models.ForeignKey(Tweet, null=True, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profiles, null=True, on_delete=models.CASCADE)
    retwitted_by = models.ManyToManyField(Profiles, related_name="retweet_users")
    likes_users = models.ManyToManyField(Profiles, related_name="likes_tweets")
    