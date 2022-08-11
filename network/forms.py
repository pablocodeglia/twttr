from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={"rows":4, "cols":10, "placeholder": "Type your message here..."}))

    class Meta:
        model = Post
        fields = ['body']