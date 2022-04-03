from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session


# Create your models here.
class comment(models.Model):
    Rating_Choices = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'), ]

    comment = models.TextField()
    # image = models.ImageField(upload_to='images/', null=True, blank=True)
    rating = models.IntegerField(choices=Rating_Choices)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + '--' + str(self.movie_id)


class poster(models.Model):
    image_id = models.IntegerField(default=-1)
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=128, blank=True)
    uploader = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    movie_id = models.IntegerField(null=False,blank=False)
    movie_title=models.CharField(max_length=200,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.movie_title + '--' + self.user.username


class WishList(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def __str__(self):
    return self.user.username + '--' + str(self.movie_id)
