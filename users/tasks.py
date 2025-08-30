from celery import shared_task
from .utils import TaskWithOnCommit
from .models import User
from .utils import EmailSender

@shared_task
def send_forgot_password_otp(email,full_name,otp_code,time): 
    email_sender_obj = EmailSender('Computerhubuk Forgot Password OTP')
    try:
        email_sender_obj.send_otp_email(email=email,full_name=full_name,otp_code=otp_code,time=time)
        return f"Sending email to {email}"
    except Exception as exc:
        return f"Failed to send email to {email}. Exception occured."
          
send_forgot_password_otp = TaskWithOnCommit(send_forgot_password_otp)


@shared_task
def send_confirmation_email(endpoint,email,first_name):
    
    email_sender_obj = EmailSender('Computer Hub Email Confirmation and Password set  Link')
    try:
        email_sender_obj.send_confirm_email(endpoint=endpoint,email=email,first_name=first_name)
        return f"Sending email to {email}"
    except Exception as exc:
        return f"Failed to send email to {email}. Exception occured."
          
send_confirmation_email = TaskWithOnCommit(send_confirmation_email)



