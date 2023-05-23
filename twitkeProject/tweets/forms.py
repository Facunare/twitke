from django.forms import ModelForm
from .models import Tweet
from django.forms import CharField
from emoji_picker.widgets import EmojiPickerTextInputAdmin, EmojiPickerTextareaAdmin
class postTweet(ModelForm):
    long_text = CharField(widget=EmojiPickerTextareaAdmin)
    class Meta:
        model = Tweet
        fields = ['content']