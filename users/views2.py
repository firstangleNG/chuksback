from django.shortcuts import render ,redirect,get_object_or_404
from django.contrib import messages
from .models import User
from django.core.exceptions import ValidationError
import phonenumbers
from django.contrib.auth import authenticate, login,logout
from django.db.models import Q
from users.tasks import send_confirmation_email,send_forgot_password_otp
from .utils import get_otp,verify_otp_code,generate_random_string,get_otp_for_forgot_password
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

        if not email and not phone_number:
            messages.error(request, "Either Email or Phone Number is required.")
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
    # print(request.user.is_authenticated)
    # if request.user.is_authenticated:
    #     return redirect('ticket')  
    if request.method == "POST":
        email_or_phone = request.POST.get("email-or-phone", "")
        password = request.POST.get("password")
        
        if not email_or_phone:
            messages.error(request, "Email or phone number is required")
            return render(request, "login.html")
        
        if not password:
            messages.error(request, "Password is required")
            return render(request, "login.html")
        user = authenticate(request, username=email_or_phone, password=password)
        if user is not None:
            login(request, user)
            # return redirect("ticket_list") 
            # return redirect(reverse("ticket_list", kwargs={"user_id": user.pk}))
               # Ensuring the UUID is converted to a string
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
        
        user = get_object_or_404(User,email=email)
        if user is None:
            messages.error(request,"No user with thie email address exists.")
            return render(request,'enter-email-for-forgot-password.html')
        
        otp = get_otp_for_forgot_password()
        time = 300
        if settings.DEBUG == True:
            print("Your OTP is : ",otp)
            # User password when DEBUG is True is changed mannually cusing django_extensions runcrsipt command in scripts folder
            redis_object.setex(f"token_for_{otp}",time+1,str(request.user.pk)) # I added 1 second to the expiry of the otp
            return redirect(reverse("set_forgot_password",kwargs={"id":user.pk}))
        else:
                # send an email confirmation message process to celery 
                send_forgot_password_otp.delay_on_commit(email=user.email,first_name=user.full_name,otp_code=otp,time=time)
                redis_object.setex(f"token_for_{otp}",time+1,str(user.pk)) # I added 1 second to the expiry of the otp    
                return redirect(reverse("set_forgot_password",kwargs={"id":user.pk}))
    return render(request,"enter-email-for-forgot-password.html")
    

def set_forgot_password(request,id):
    return render(request,'set-forgot-password.html')
