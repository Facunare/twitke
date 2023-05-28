from django.forms import ModelForm
from .models import Tweet
from django.forms import CharField
class postTweet(ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']