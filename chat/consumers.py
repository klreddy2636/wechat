import time
import datetime
import json
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import render
from asgiref.sync import async_to_sync
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
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
        user_list = room_user_data.get(self.room_group_name, [])
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

        if room_name not in room_user_data:
            room_user_data[room_name] = []
        if username not in room_user_data[room_name]:
            room_user_data[room_name].append(username)
    def remove_user_from_room(self, room_name, username):
        
        if room_name in room_user_data and username in room_user_data[room_name]:
            room_user_data[room_name].remove(username)
         




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
