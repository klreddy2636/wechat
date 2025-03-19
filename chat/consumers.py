import time
from datetime import datetime
import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from django.shortcuts import render
from asgiref.sync import async_to_sync
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from chat.models import *
from chat.models import Chat
global_room_user_data={}
room_user_data={}
class MyConsumer(WebsocketConsumer):
    # permission_classes = [IsAuthenticated]
    # authenticated = [JWTAuthentication]
   
    def connect(self):
        print("COnnecting web scokcets")
        self.room_group_name = 'test'
        print("The channel name is ",self.channel_name)
        print("The group name is ",self.room_group_name)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        print("The user is ",self.scope.get('user'))
        self.username = str(self.scope.get('user'))
        self.add_user_to_room(self.room_group_name, self.username)
        self.send_user_list_and_count()
       
        print("The User is ",self.scope.get('user'))
        self.user = self.scope.get('user')
        self.accept()
       
        # self.send(text_data=json.dumps({
        #     'type':'connection_established',
        #     'message': 'Hello'
        # }))
       
    # async def disconnect(self, code):
    #     print("Youre disconnected")
    def receive(self, text_data=None, bytes_data=None):
        print("The recieved text data")
        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = str(self.user.username)
        self.send_user_list_and_count()
 
        print("The channel name is ",self.channel_name)
        print("The group name is ",self.room_group_name)
        print("The user is ",username)
        print("The scopped user is ",self.scope.get('user'))
        print("Self . user is", self.user)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message': message,
                'user': username,
                'channel_name':self.channel_name,
                'group_name':self.room_group_name,
            }
        )
 
    def disconnect(self, close_code):
        # Remove the user from the group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )
 
        # Decrement the user count for the room
        self.remove_user_from_room(self.room_group_name, self.username)
        self.send_user_list_and_count()
 
    def send_user_list_and_count(self):
        # Get the current user count for the room
        user_list = global_room_user_data.get(self.room_group_name, [])
        user_count = len(user_list)
 
        # Send the user count to the group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'user_list_update',
                'user_list': user_list,
                'user_count': user_count,
            }
        )
 
    def add_user_to_room(self, room_name, username):
 
        if room_name not in global_room_user_data:
            global_room_user_data[room_name] = []
        if username not in global_room_user_data[room_name]:
            global_room_user_data[room_name].append(username)
    def remove_user_from_room(self, room_name, username):
       
        if room_name in global_room_user_data and username in global_room_user_data[room_name]:
            global_room_user_data[room_name].remove(username)
         
 
 
 
 
    def chat_message(self, event):
        message = event['message']
        time_stamp=time.time()
        time_stamp = time.strftime('%H:%M:%S', time.localtime(time_stamp))
        print("Timestamp of the message received:", time_stamp)
        user = event['user']
        print("The user fromt he event message is ",user)
        print("The username is *****",self.user.username)
        self.send(text_data=json.dumps({
            'type':'message_received',
            'message': message,
            'timestamp': time_stamp,
            'username': user,
        }))
 
    def user_list_update(self, event):
        user_list = event['user_list']
        user_count = event['user_count']
        self.send(text_data=json.dumps({
            'type': 'user_count',
            'user_list': user_list,
            'user_count': user_count,
        }))
 
 
 
 
 
 
 
        # print(message)
        # self.send(text_data=json.dumps({
        #     'type':'message_received',
        #     'message': f'You sent: {message}'
        # }))
 
 
class PersonalChat(WebsocketConsumer):
    def connect(self):
        self.group_name = self.user.id
 
 
 
 
class GroupChat(WebsocketConsumer):
    def connect(self):
        print("Connecting to group chat...")
       
        # Get room name from the URL route kwargs
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"group_{self.room_name}"
       
        # Add the channel to the group
        async_to_sync (self.channel_layer.group_add)(
 
            self.room_group_name,
            self.channel_name
        )
       
 
        self.username = str(self.scope.get('user'))
        self.user = self.scope.get('user')
        # Accept the WebSocket connection
        self.accept()
 
        # Send a message indicating successful connection
        self.send(text_data=json.dumps({
            'type': 'group_created',
            'message': f"Connected to {self.room_name}!"
        }))
 
    def receive(self, text_data):
        # Receive the message from WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']
        user2 = str(self.user.username)
        print("Received message:", message)
 
        # Send the message to the group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user':user,
                'user2': user2
            }
        )
 
 
 
    def chat_message(self, event):
        # This method is triggered when a message is received from the group
        print(event)
        message = event['message']
        user = event['user']
        user2 = event['user2']
        print("Sending message to WebSocket:", message)
 
        # Send the message to the WebSocket
        self.send(text_data=json.dumps({
            'type': 'chat',
            'text': message,
            'user':user,
            'user2':user2
        }))
 
    def disconnect(self, close_code):
        # Remove the channel from the group when it disconnects
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"Disconnected from {self.room_name}")
 
 
 
 
 
 
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user1_id = self.scope['url_route']['kwargs']['user1_id']
        self.user = self.scope.get('user')
        self.room_name = f"chat_{min(int(self.user1_id), int(self.user.id))}_{max(int(self.user1_id), int(self.user.id))}"
        print(self.room_name)
        print("Room name")
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
 
        await self.accept()
        self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': f"Connected to {self.room_name}!"
        }))
 
    async def disconnect(self, close_code):
 
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )
 
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = self.scope.get('user')
        print("THe sender is",sender.username)
        #try:
            #receiver = User.objects.get(id=self.user1_id)  # Ensure you use the correct ID here
        #except User.DoesNotExist:
        #    print(f"User with ID {self.user1_id} not found")
        
        #chat_message = Chat(sender=sender,receiver=self.user1_id, message=message, created_at=datetime.now())
        # if self.user == self.user1_id:
        #     chat_message = Chat(sender=sender,reciever=self.user2_id, message=message, created_at=datetime.now())
        # else:
        #     chat_message = Chat(sender=sender,reciever=self.user1_id, message=message, created_at=datetime.now())
        #chat_message.save()
 
 
        await self.channel_layer.group_send(
            self.room_name,{
                'type': 'chat_message',
                'message': message,
                'user':sender.username,
            }
        )
        print("Message sent to group")
 
    async def chat_message(self, event):
        print("Inside chat messgae dfucniton")
        time_stamp=time.time()
        time_stamp = time.strftime('%H:%M:%S', time.localtime(time_stamp))
        print("Timestamp of the message received:", time_stamp)
        message = event['message']
        sender = event['user']
        print("The message sent is ",message)
 
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'user': sender,
            'time_stamp': time_stamp
        }))
