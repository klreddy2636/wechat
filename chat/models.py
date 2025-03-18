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
    friendsrequested = models.ManyToManyField(User, related_name='friendsrequested', blank=True)
    def __str__(self):
        return self.username
    
class Chat(models.Model):
    sender = models.OneToOneField(User, on_delete=models.CASCADE,blank=True,null=True)
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reciever',blank=True,null=True)
    message = models.TextField()
    type = models.CharField(choices={'private':'private','public':'public'},max_length=20,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
    def __str__(self):
        return self.message
    

class Rooms(models.Model):
    room_name = models.CharField(max_length=255)
    users = models.ManyToManyField(UserProfile, related_name='rooms')
    created_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.room_name
    

