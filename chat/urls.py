from django.urls import path
from chat.views import *

urlpatterns = [
    path('', HomeView.as_view(), name='main'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('people/', PeopleView.as_view(), name='people'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('about/', AboutView.as_view(), name='about'),
    path('API/profile/',ProfileUpdate.as_view(), name='profileupdate'),
    path('API/verify_token/', VerifyTokenView.as_view(), name='verify_token'),
    path('API/people/', PeopleAPIView.as_view(), name='people'),
    path('API/frndrqst/', FriendRequestAPIView.as_view(), name='friendrequest'),
    ]