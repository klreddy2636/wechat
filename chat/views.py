from django.shortcuts import render
from django.views import View
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

from rest_framework.views import APIView

from chat.models import Rooms, UserProfile
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

from chat.serializers import RoomSerializer, UserProfileSerializer

class VerifyTokenView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
 
    def get(self, request):
        print("The user is ",request.user)
        user= request.user
        allUsers = UserProfile.objects.all()
        users = UserProfileSerializer(allUsers,many=True)
        user_profile = UserProfile.objects.get(user=user)
        user_profile=UserProfileSerializer(user_profile)
        return Response({'user_profile': user_profile.data , 'allUsers':users.data}, status=status.HTTP_200_OK)
        # try:
        #     return Response({'message': 'Token is valid'}, status=status.HTTP_200_OK)
        # except AuthenticationFailed:

        #     return Response({'message': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)


class HomeView(View):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication, SessionAuthentication, BasicAuthentication]
    def get(self, request):
        
        return render(request, 'home.html')
    

class UserprofileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication, SessionAuthentication, BasicAuthentication]
    def get(self, request):
        user = request.user
        user_profile = user.objects.get(user=user)
        return Response({"user_profile": user_profile})
    
class LoginView(APIView):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        print(username, password)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({
            'access_token':access_token
        })
    
import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import View

class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            if not username or not password:
                return JsonResponse({"error": "Username and password are required!"}, status=400)

            # Create the user
            user = User.objects.create_user(username=username, password=password)
            user_profile = UserProfile.objects.create(user=user, username=username, email=email)
            return JsonResponse({"message": "User created successfully!"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class PeopleView(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'people.html', {'users': users})

class PeopleAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication, SessionAuthentication, BasicAuthentication]
    def get(self, request):
        user= request.user
        users = UserProfile.objects.exclude(user=user)
        user_profile = UserProfile.objects.get(user=user)
        
        friends = user_profile.friends
        friends = UserProfileSerializer(friends,many=True)
        print("The users friends are: ",friends.data)
        friendsrequested = user_profile.friendsrequested

        friendrequests = user_profile.friendrequests

        friendrequests = UserProfileSerializer(friendrequests,many=True)
        print("The friend requests are",friendrequests.data)

        
        friendsrequested = UserProfileSerializer(friendsrequested, many=True)
        print("The users requested are ",friendsrequested.data)
        users = UserProfileSerializer(users, many=True)
        
        return Response({"user_profiles": users.data, "friends": friends.data, "friendsrequested": friendsrequested.data,"friendrequests": friendrequests.data})


class ProfileView(View):

    def get(self, request):
        return render(request, 'profile.html')
    def post(self, request):
        user = request.user

class ProfileUpdate(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication, SessionAuthentication, BasicAuthentication]
    def get(self, request):
        print("The user was is ",request.user)
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.profile_pic:
            print("THe user profiel picture is ",user_profile.profile_pic)
            profile_pic_url = request.build_absolute_uri(user_profile.profile_pic.url)
        else:
            profile_pic_url = None
        return Response({"username": user_profile.username, 
                         "email": user_profile.email,
                         "bio": user_profile.bio,
                         "profile": profile_pic_url})
    def post(self, request):
        user = request.user
        print("THe user is this guy",user.username)
        user_profile = UserProfile.objects.get(user=request.user)
        print("THe user profiel picture is ",user_profile.username)
        print("THe passo is ",request.data.get('password'))
        try:
            user=authenticate(username=user.username, password=request.data.get('password'))
            print("THe user is authenticated :",user)
            if user:
                print("The user is authenticated")
                if request.data.get('username')!=None:
                    user_profile.username = request.data.get('username')
                if request.data.get('email')!=None:
                    user_profile.email = request.data.get('email')
                if request.data.get('bio')!=None:
                    user_profile.bio = request.data.get('bio')
                if request.data.get('profile_pic')!=None:
                    user_profile.profile_pic = request.data.get('profile_pic')
                user_profile.save()

        except:
            return Response({"error": "Invalid password!"}, status=400)
        
        return Response({"message": "Profile updated successfully!"})



class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')
    
class FriendRequestView(View):
    def get(self, request):
        
        return render(request, 'requests.html')


class FriendRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication, SessionAuthentication, BasicAuthentication]
    def get(self, request):
        user= request.user
        print("The user is %s" % user)
        friend_requests = UserProfile.objects.get(user=user).friendrequests
        print("Friend requests: ",friend_requests)
        
        friend_requests = UserProfileSerializer(friend_requests, many=True)
        return Response({"requests": friend_requests.data})
    
    def post(self, request):
        user= request.user
        user_id = request.data.get('addFriend')
        user_profile = UserProfile.objects.get(user=user)

        friend = request.data.get('addFriend')
        print("The id is: ",user_id)
        friend = UserProfile.objects.get(id=friend)
        friend = friend.user
        print("The friend is: ",friend)
        if friend:
            friend = UserProfile.objects.get(user=friend)
            print("The firend is ",friend)
            if friend not in user.friends.all():
                user_profile.friendsrequested.add(friend.user)
                friend.friendrequests.add(user)
                friend.save()
            else:
                return Response({"error": "Hes Already a Friedn!"}, status=400)

        
            return Response({"success": "Friend request sent successfully!"})
        else:
            return Response({"error": "User not found!"}, status=404)
        


class FriendsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication, SessionAuthentication, BasicAuthentication]

    def get(self, request):
        user= request.user
        print("The user is %s" % user)
        friends = UserProfile.objects.get(user=user).friends
        
        friends = UserProfileSerializer(friends, many=True)
        return Response({"friends": friends.data})
    def post(self,request):
        user= request.user
        user_id = request.data.get('addFriend')
        friend = User.objects.get(user=user_id)
        print("The id is: ",user_id)
        user = UserProfile.objects.get(user=user)
        UserProfile.friends.add(friend)
        UserProfile.friendrequests.remove(friend)
        print("The firends are",user.friends)
        
    def put(self,request):
        ##** Here the request user is accepting friend request
        ##** The friend has requested it so adding him to friends and removing the request
        user= request.user
        user_profile = UserProfile.objects.get(user=user)
        friend_id = request.data.get('addFriend')
        friend = User.objects.get(id=friend_id)
        print("The id is: ",friend_id)
        if friend:
            print("Inside Friend",friend)
            friend = UserProfile.objects.get(user=friend)
            print("The firend is ",friend.username)
            user_profile.friends.add(friend.user)
            friend.friends.add(user)
            friend.friendsrequested.remove(user_profile.user)
            user_profile.friendrequests.remove(friend.user)
            
            friend.save()
            return Response({"success": "Friend added successfully!"})
        else:
            return Response({"error": "User not found!"}, status=404)
        


def Room(request,room_name):
    print("room_name:----------- ",room_name)
    return render(request, 'Room.html', {'room_name': room_name})



class CreateRoomView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
 
    def get(self,request):
        user_id = request.user.id
        print("user_id:----------- ",user_id)
        user_id = UserProfile.objects.get(user__id = user_id)
        print("user_id:----------- 2",user_id.id)
        rooms = Rooms.objects.filter(users__id=user_id.id)
        print("rooms------------roomms",rooms)
        rooms = RoomSerializer(rooms , many=True)
        print(rooms)
 
        return Response({'rooms': rooms.data})
    def post(self, request, *args, **kwargs):
        room_name = request.data.get("room_name")
        user_ids = request.data.get("users", [])
        print("user_ids:----------- ", user_ids)
        if not room_name or not user_ids:
            return Response(
                {"error": "Room name and users are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
 
        # Get user instances for the provided IDs
        users = []
        print("----------------------",request.user)
        try:
            creator = UserProfile.objects.get(user=request.user)
            print('creator',creator)
            users.append(creator)
        except UserProfile.DoesNotExist:
            print(f"User with id {request.user.id} not found.")
 
        for id in user_ids:
            user = UserProfile.objects.get(id=id)
            users.append(user)
        print('users',users)
       
 
        room = Rooms.objects.create(room_name=room_name)
        print('rooms',room)
        room.users.add(*users)  # Add users to the room's many-to-many field
       
        return Response({
            'success': True,
            'message': 'Room created successfully!',
            'room': RoomSerializer(room).data
        }, status=status.HTTP_201_CREATED)
 






class RoomDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,*args,**kwargs):

        room=request.query_params.get("room_name")
        print("The rorom name is",room)

        if not room:
            return Response({"error": "room_name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            room = Rooms.objects.get(room_name=room)
            print("Got the rrom object",room.users)
        except Rooms.DoesNotExist:
            return Response({"error": "Room Not OFund"}, status=status.HTTP_404_NOT_FOUND)
        users=room.users.all()
        users = UserProfileSerializer(users,many=True)
        print("THe users are ",users)
        
        return Response({
            'users': users.data
        })
