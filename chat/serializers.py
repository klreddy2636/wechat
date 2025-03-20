
from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    users=UserProfileSerializer(many=True)
    class Meta:
        model=Rooms
        fields='__all__'


class ChatSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    class Meta:
        model = Chat
        fields = '__all__'
