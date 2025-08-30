import threading
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import BadHeaderError
from smtplib import SMTPException
import socket
from django.conf import settings

class EmailSender:
    def __init__(self, subject, from_email=settings.EMAIL_HOST_USER):
        self.subject = subject
        self.from_email = from_email

    def send_email_async(self, html_content, text_content, to):
        try:
            email = EmailMultiAlternatives(self.subject, text_content, self.from_email, [to])
            email.attach_alternative(html_content, "text/html")
            email.send()
        except BadHeaderError:
            print("Invalid header found in the email.")
        except SMTPException as e:
            print(f"SMTP error occurred: {e}")
        except socket.gaierror:
            print("Network error: Unable to connect to the mail server.")
        except TimeoutError:
            print("Timeout error: The connection to the mail server timed out.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        except ConnectionError as e:  
            print(f"Connection error occurred: {e}")  

    def _start_email_thread(self, html_content, text_content, to):
        email_thread = threading.Thread(target=self.send_email_async, args=(html_content, text_content, to))
        email_thread.start()

    def send_confirm_email(self,endpoint,email,first_name):
        try:
                to = email
                html_content = render_to_string('confirm_email.html', {
                    'endpoint':endpoint,
                    "email":email  ,
                    'first_name':first_name
                                      
                })
                text_content = strip_tags(html_content)
                self._start_email_thread(html_content, text_content, to)
        except BadHeaderError:
            ("Invalid header found in the email.")
        except SMTPException as e:
            return(f"SMTP error occurred while sending the forgot password email: {e}")
        except socket.gaierror:
            return("Network error: Unable to connect to the mail server.")
        except TimeoutError:
            return("Timeout error: The connection to the mail server timed out.")
        except ConnectionRefusedError:
            return("The connection was refused by the mail server.")
        except socket.error as e:
            return(f"Socket error: {e}")
        except Exception as e:
                return(f"An unexpected error occurred: {e}")
         

    def send_otp_email(self,email, full_name, otp_code,time):
        to = email
        html_content = render_to_string('frogot-password-otp.html', {
            'email': email,
            'full_name': full_name,
            'otp_code': otp_code,
            'time': time
        })
        text_content = strip_tags(html_content)
        self._start_email_thread(html_content, text_content, to)

    
# Usage Example
# email_sender = EmailSender(subject='Reset Your Password')
# email_sender.send_forgot_password_link(request, email, user_id, first_name, token)




from django.db import transaction

class TaskWithOnCommit:
    def __init__(self, task):
        """
        Initializes the wrapper class with a Celery task.
        :param task: A Celery task function.
        """
        self.task = task

    def delay_on_commit(self, *args, **kwargs):
        """
        Schedules the task to run after the transaction is committed.
        :param args: Arguments to be passed to the task.
        :param kwargs: Keyword arguments to be passed to the task.
        """
        # Use Django's transaction.on_commit to delay the task execution
        transaction.on_commit(lambda: self.task.delay(*args, **kwargs))


from rest_framework.permissions import BasePermission
from .models import User
from rest_framework.response import Response
import redis 

class HasValidTokenVersion(BasePermission):
    redis_obj = redis.StrictRedis(host="localhost",port=6379,password="",decode_responses=True)
    def has_permission(self, request, view):
        user = User.objects.filter(id=request.user.pk).first()
        if request.auth.get("token_version",None)  is None:
            return Response(data={"detail":"No token version provided"})
        elif request.auth.get("token_version",None) == user.token_version:
            return True
        else: 
            return False
        
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import login

class ValidateAccessToken(BasePermission):
    def has_permission(self, request, view):
        """
        Custom Permission Class to validate access token before accessing the protected view.
        """
        # Get access token from cookies
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            raise AuthenticationFailed(_("Access token is missing."))

        try:
            # Decode and validate the token using Simple JWT
            token = AccessToken(access_token)
            # Print token for debugging purposes
            user_id = token.payload.get('user_id') #The user_id is the value set as  "USER_ID_CLAIM" : "user_id" in  SIMPLE_JWT in settings.py
            user = User.objects.filter(id=user_id).first()
            request.user = user          
            return True
        
        except Exception as e:
            print(str(e))
            raise AuthenticationFailed(_("Token validation failed: " + str(e)))


import pyotp

key = pyotp.random_base32()  # Generate a unique key for each user
code = pyotp.TOTP(key,interval=86400)

def get_otp():
    return code.now()


def verify_otp_code(otp:str):
    return code.verify(otp,valid_window=0)




key_for_forgot_password_otp = "TelleveryonethatthekingdomofGodishere"
code_for_forgot_password = pyotp.TOTP(key_for_forgot_password_otp,interval=300)

def get_otp_for_forgot_password():
    return code_for_forgot_password.now()


def verify_otp_code_for_forgot_password(otp:str):
    return code_for_forgot_password.verify(otp,valid_window=0)





import random
import string

def generate_random_string(length):
    # Use string.ascii_letters for letters (lowercase and uppercase) and string.digits for digits
    symbols = ["$", "%", "&", "(", "#", ")"]
    characters = string.ascii_letters + string.digits + random.choice(symbols)
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


