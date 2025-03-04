from django.db import models

from django.contrib.auth.models import User 
# Create your models here.



class Chat(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.message

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    friendrequests = models.ManyToManyField(User, related_name='friendrequests', blank=True)

    def __str__(self):
        return self.user.username
    

