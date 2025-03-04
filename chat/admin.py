from django.contrib import admin

from chat.models import Chat, UserProfile
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Chat)
admin.site.register(UserProfile)
