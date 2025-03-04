import jwt
from channels.auth import AuthMiddlewareStack
from django.conf import settings
from channels.db import database_sync_to_async
from channels.exceptions import DenyConnection
from django.contrib.auth import get_user_model
 
class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner
 
    async def __call__(self, scope, receive, send):
        token = None
        query_string = scope.get('query_string', b'').decode()
        if 'token=' in query_string:
            token = query_string.split('=')[1]
       
        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user_id = payload.get('user_id')
                user = await database_sync_to_async(self.get_user)(user_id)
                if user is None:
                    raise DenyConnection("Invalid user.")
                scope["user"] = user
            except jwt.ExpiredSignatureError:
                raise DenyConnection("Token has expired.")
            except jwt.DecodeError:
                raise DenyConnection("Invalid token.")
        else:
            raise DenyConnection("JWT token is required for authentication.")
 
        return await self.inner(scope, receive, send)
 
    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None











# # your_app_name/middleware.py
# import jwt
# from channels.auth import AuthMiddlewareStack
# from channels.exceptions import DenyConnection
# from django.conf import settings
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from channels.db import database_sync_to_async
# from django.contrib.auth.models import User


# class JWTAuthMiddleware:
#     """
#     WebSocket middleware to authenticate JWT token passed in the WebSocket handshake.
#     """

#     def __init__(self, inner):
#         self.inner = inner

#     async def __call__(self, scope, receive, send):
#         # Get the token from the WebSocket handshake headers
#         token = None
#         for param in scope.get("headers", []):
#             if param[0] == b"authorization":
#                 token = param[1].decode().split(" ")[1]
#                 break

#         if token is None:
#             raise DenyConnection("JWT token is required for authentication.")

#         # Authenticate the user using the token
#         try:
#             # Validate the JWT token and extract user info
#             user = await self.get_user_from_token(token)
#             scope["user"] = user
#         except Exception as e:
#             raise DenyConnection(f"Invalid JWT token: {str(e)}")

#         return await self.inner(scope, receive, send)

#     @database_sync_to_async
#     def get_user_from_token(self, token):
#         """
#         Helper function to validate the JWT token and retrieve the user
#         """
#         try:
#             # Decode the JWT token
#             decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#             user_id = decoded_token.get("user_id")

#             if user_id is None:
#                 raise Exception("Invalid token: user_id missing.")

#             user = User.objects.get(id=user_id)
#             return user
#         except jwt.ExpiredSignatureError:
#             raise Exception("Token has expired.")
#         except jwt.InvalidTokenError:
#             raise Exception("Invalid token.")
#         except User.DoesNotExist:
#             raise Exception("User does not exist.")
#         except Exception as e:
#             raise Exception(f"Error decoding the token: {str(e)}")