from django.contrib import admin
from .models import User 

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "phone_number", "is_active","full_name", "created_at") 
    readonly_fields = ("created_at",) 
    fieldsets = (
        (None, {"fields": ("full_name","email", "phone_number", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login",)}), 
    )

admin.site.register(User, CustomUserAdmin)
