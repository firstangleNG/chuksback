from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.utils import timezone
import os
import uuid
import phonenumbers


class UserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        """
        Create and return a regular user with either phone_number or email and a password.
        """
        if not email or not phone_number:
            raise ValueError("Both email and phone number must be set")
        if not password:
            raise ValueError("You must provide a password")

        phone_number = self.normalize_phone(phone_number) if phone_number else None

        user = self.model(
            email=self.normalize_email(email) if email else None,
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone_number=None, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError('Either email or phone number must be set for admin users')

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('role', "admin")
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, phone_number, password, **extra_fields)

    def normalize_phone(self, phone_number: str):
        """
        Normalize and validate a phone number using the phonenumbers library.
            """
        if not phone_number:
            return None

        phone_number = phone_number.strip()

        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            
            # DEBUG: Print the parsed details
            print(f"Parsed Number: {parsed_number}")
            
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError(f"Invalid phone number: {phone_number}")

            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)

        except phonenumbers.NumberParseException:
            raise ValueError(f"Invalid phone number format: {phone_number}")



def unique_image_path(instance, filename):
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join("profile_pictures/", unique_filename)


def default_profile_picture():
    return 'profile_pictures/default.jpg'  # Relative to MEDIA_ROOT


class User(AbstractBaseUser, PermissionsMixin):    
    ROLE_CHOICES = [
        ("superadmin", "Super Admin"),
        ("admin", "Admin"),
        ("technician", "Technician"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,unique=True)
    email = models.EmailField(max_length=150, unique=True)
    full_name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="technician")

    phone_number = models.CharField(
        max_length=16, unique=True, blank=True, null=True,
        validators=[
            RegexValidator(
                regex=r'^\+[1-9]\d{6,14}$',
                message="Enter a valid phone number with country code (e.g., +14155552671)"
            )
        ]
    )

    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", default=default_profile_picture, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['phone_number']  

    objects = UserManager()

    def __str__(self):
        return f"{self.email}" 




