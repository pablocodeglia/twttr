from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('User', related_name='following_list', default=None, blank=True)
    followers = models.ManyToManyField('User', related_name='followers_list', default=None, blank=True)

    def __str__(self):
        return self.username

class Post(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    body = models.CharField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='like', default=None, blank=True)
    likes_num = models.IntegerField(default=0)

    def __str__(self):
        return f'{str(self.user).capitalize()} said: "{self.body}"'
    

class Like(models.Model):
    liker = models.ForeignKey('User', related_name='liker', on_delete=models.CASCADE)
    liked_post = models.ForeignKey('User', related_name='liked_post', on_delete=models.CASCADE)


