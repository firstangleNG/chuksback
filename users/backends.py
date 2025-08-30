from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailAuthBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using only their email.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)  # Use email instead of username
        except User.DoesNotExist:
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None






# from django.contrib.auth.backends import BaseBackend
# from django.contrib.auth import get_user_model
# from django.db.models import Q
# import logging


# User = get_user_model()

# class EmailOrPhoneBackend(BaseBackend):
    
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         # Ensure username and password are provided
#         if not username or not password:
#             return None

#         # Fallback to ModelBackend for admin login
#         if request and request.path == '/admin/login/':
#             return None  # Pass control to the next backend

#         # Attempt to find the user by email or phone number
#         try:
#             user = User.objects.get(Q(email=username) | Q(phone_number=username))
#         except User.MultipleObjectsReturned:
#             return None
#         except User.DoesNotExist:
#             return None

#         # Validate the password and check user status
#         if user.check_password(password) and self.user_can_authenticate(user):
#             return user
#         return None

#     def user_can_authenticate(self, user):
#         """Check if the user is active and eligible for authentication."""
#         return user.is_active

