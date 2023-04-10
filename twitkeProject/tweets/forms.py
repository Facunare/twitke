from django.forms import ModelForm
from .models import Tweet

class postTweet(ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']