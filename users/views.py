from django.shortcuts import render ,redirect,get_object_or_404
from django.contrib import messages
from .models import User
from django.core.exceptions import ValidationError
import phonenumbers
from django.contrib.auth import authenticate, login,logout
from django.db.models import Q
from users.tasks import send_confirmation_email,send_forgot_password_otp
from .utils import get_otp,verify_otp_code,generate_random_string,get_otp_for_forgot_password,get_otp_for_forgot_password,verify_otp_code_for_forgot_password
import redis
from django.conf import settings
from django.contrib.auth.hashers import make_password
from customers.models import Customer
from django.urls import reverse

redis_object = redis.Redis(host="localhost",port=6379,decode_responses=True)


def create_user(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()
        role = request.POST.get("role", "technician")
        address = request.POST.get("address", "").strip()
        profile_picture = request.FILES.get("profile_picture", None)

        # Check required fields**
        if not full_name:
            messages.error(request, "Full name is required.")
            return render(request, "add_user.html")

        if not email or not phone_number:
            messages.error(request, "Either Email and Phone Number is required.")
            return render(request, "add_user.html")

        # Validate email 
        if email and User.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return render(request, "add_user.html")
        
          # Validate phone number. check if already used  
        if email and User.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "Phone number  is already in use.")
            return render(request, "add_user.html")

        # Validate phone number format
        if phone_number:
            try:
                parsed_number = phonenumbers.parse(phone_number, None)
                if not phonenumbers.is_valid_number(parsed_number):
                    messages.error(request, "Invalid phone number format.")
                    return render(request, "add_user.html")
            except phonenumbers.NumberParseException:
                messages.error(request, "Invalid phone number format.")
                return render(request, "add_user.html")


        # Create user
        user = User(
            full_name=full_name,
            email=email or None,
            phone_number=phone_number or None,
            role=role,
            address=address,
            profile_picture=profile_picture
        )
        generated_password = generate_random_string(12)
        user.set_password(generated_password)  # Hash password before saving
        user.save()
        # send otp
        if settings.DEBUG==True: 
            messages.success(request, f"User created successfully!. Your password is :{generated_password}  ")
        else:
       # Send confirmation email in production mode
             scheme = request.scheme
             host = request.get_host()
             otp = get_otp()
             endpoint = f"{scheme}://{host}/accounts/verify-email/?token={otp}"
             first_name = full_name.split()[0] if isinstance(full_name, str) and full_name.strip() else full_name
             send_confirmation_email.delay_on_commit(
                     endpoint=endpoint,
                     email=user.email,
                     first_name=first_name
                     )
                  # Save OTP to Redis with a 1-day expiration
             redis_object.setex(f"token_for_{otp}", 86400, str(user.pk))
        
             messages.success(request, "User created successfully! The user will receive an email soon in other to active their account ")
    return render(request, "add_user.html",{})

 

import uuid
def verify_email_link(request):
    token = request.GET.get("token")  # Get token from the URL

    if not token:
        messages.error(request, "Invalid or missing verification token.")
        return redirect("otp_verification_error")  
    
    try:
        user_id = redis_object.get(f"token_for_{token}")
        user_id_uuid = uuid.UUID(user_id)  # Convert string to UUID
        if user_id_uuid is None:
            messages.error(request, "Invalid or expired  OTP.")
            return redirect("otp_verification_error")
        
        if verify_otp_code(otp=token): 
            user = User.objects.filter(id=user_id_uuid).first()
            if user:
                messages.success(request, "OTP verified successfully.")
                return redirect(reverse("set_password", kwargs={"id": user.pk}))
                # return redirect("set_password",user.pk)
            messages.error(request, "Invalid user ID.")
            return redirect("otp_verification_error")
        messages.error(request, "Invalid OTP.")
        return redirect("otp_verification_error")
    
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("otp_verification_error")
    




from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

def set_new_password(request, id):
    """
    View to handle setting a new password after OTP verification.
    """
    user = get_object_or_404(User, id=id)

    # Ensure the user is inactive before allowing a password reset
    if user.is_active:
        messages.error(request, "This user account is already active. Resetting password is not allowed.")
        return redirect("login")

    if request.method == "POST":
        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        if not password or not confirm_password:
            messages.error(request, "Password fields cannot be empty.")
            return render(request, "set_password.html", {"id": id})

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, "set_password.html", {"id": id})

        try:
            validate_password(password, user=user)  # Enforce strong password rules
        except ValidationError as e:
            messages.error(request, "; ".join(e.messages))
            return render(request, "set_password.html", {"id": id})

        user.password = make_password(password)
        user.is_active = True  # Activate user after password is set
        user.save(update_fields=["password", "is_active"])  # Update only necessary fields

        messages.success(request, "Your password has been set successfully. Please log in.")
        return redirect("login")
    
    return render(request, "set_password.html", {"id": id})



def login_user(request):
      # If the user is already authenticated, redirect them to the ticket area
    if request.user.is_authenticated:
        return redirect("dashboard") 
    if request.method == "POST":
        email = request.POST.get("email", "")
        password = request.POST.get("password")
        
        if not email:
            messages.error(request, "Email address is required")
            return render(request, "login.html")
        
        if not password:
            messages.error(request, "Password is required")
            return render(request, "login.html")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("ticket_list", kwargs={"user_id": str(user.pk)}))
        
        else:
            messages.error(request, "Invalid credentials")   
    return render(request, "login.html")


def logout_user(request):
    logout(request)
    messages.success(request,"You have been logged out")
    return redirect('login')

def otp_verification_error(request):
    return render(request,"otp_verification_error.html",{})




def check_forgot_password_email(request):
    if request.method == "POST":
        email = request.POST.get("email",None)
        if email is None:
            messages.error(request,"No email address provided.")
            return render(request,'enter-email-for-forgot-password.html')
        
        user = User.objects.filter(email=email).first()
        if user is None:
            messages.error(request,"No user with this email address exists.")
            return render(request,'enter-email-for-forgot-password.html')
        
        otp = get_otp_for_forgot_password()
        time = 300
        if settings.DEBUG == True:
            print("Your OTP is : ",otp)
            # User password when DEBUG is True is changed mannually cusing django_extensions runcrsipt command in scripts folder
            redis_object.setex(f"token_for_{otp}",time+1,str(user.pk)) # I added 1 second to the expiry of the otp
            # return redirect(reverse("set_forgot_password",kwargs={"id":user.pk}))
            print("PK IS : ",user.pk)
            return redirect(reverse('verify_otp_code',kwargs={"id":user.pk}))
        else:
                # send an email confirmation message process to celery 
                send_forgot_password_otp.delay_on_commit(email=user.email,full_name=user.full_name,otp_code=otp,time=time)
                redis_object.setex(f"token_for_{otp}",time+1,str(user.pk)) # I added 1 second to the expiry of the otp    
                # return redirect(reverse("verify_otp_code",kwargs={"id":user.pk}))
                print(user.pk)
                return redirect(reverse('verify_otp_code',kwargs={"id":str(user.pk)}))
    return render(request,"enter-email-for-forgot-password.html")
    


# def verify_password_reset_otp(request,id):
#     otp_token = request.POST.get('otp')
#     print("POST Data Sent from frontend :", request.POST)
#     print("OTP Sent from frontend :", otp_token)
#     if request.method == "POST":
#         if verify_otp_code(otp=otp_token): 
#             print("OTP is valid")
#             user = User.objects.filter(id=id).first()
#             if user:
#                 print("user is valid")
#                 messages.success(request, "OTP verified successfully.")
#                 return redirect(reverse("set_forgot_password", kwargs={"id": user.pk}))
#             messages.error(request, "Either user is invalid or OTP is invalid or expired.")
#             return render(request,"verify-otp.html",{"id":id}) 
#         messages.error(request,"Either user is invalid or OTP is invalid or expired.") 
#         return render(request,"verify-otp.html",{"id": id})   
#     return render(request,"verify-otp.html",{"id": id})


def verify_password_reset_otp(request, id):
    print("Received ID:", id)  # Debugging line
    otp_token = str(request.POST.get('otp')).strip()
    # print("POST Data Sent from frontend:", request.POST)
    # print("OTP Sent from frontend:", otp_token)
    if request.method == "POST":
        print("OTP Sent from frontend:", otp_token)
        if verify_otp_code_for_forgot_password(otp=otp_token):
            print("OTP is valid")
            user = User.objects.filter(id=id).first()
            if user:
                print("User is valid")
                messages.success(request, "OTP verified successfully.")
                return redirect(reverse("set_forgot_password", kwargs={"id": user.pk}))
            messages.error(request, "Either user is invalid or OTP is invalid or expired.")
            return render(request, "verify-otp.html", {"id": id})
        print("OTP is not valid")
        messages.error(request, "Either user is invalid or OTP is invalid or expired.")
        return render(request, "verify-otp.html", {"id": id})
    return render(request, "verify-otp.html", {"id": id})


def set_forgot_password(request,id):
    if request.method == "POST":
        password = str(request.POST.get("password")).strip()
        confirm_password = str(request.POST.get("confirm_password")).strip()
        if password != confirm_password: 
            messages.error(request,"Password and Confirm Password do not match")
            return render(request,'set-forgot-password.html',{"id":id})
        user = User.objects.filter(id=id).first()
        if user is None:
            messages.error(request,"Invalid user")
            return render(request,'set-forgot-password.html',{"id":id})
        else:
            
            user.set_password(password)
            user.save()
            messages.success(request,"Password changed successfully")
            return redirect('login')
    return render(request,'set-forgot-password.html',{"id":id})
