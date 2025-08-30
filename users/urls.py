from django.urls import path
from . import views 


urlpatterns = [
    path("",views.login_user,name="login"),
    path("logout/",views.logout_user,name="logout"),
    path('create-user/',views.create_user,name="create-user"),
    path('accounts/verify-email/', views.verify_email_link, name="verify_email"),
    path('new-password/<uuid:id>/',views.set_new_password,name="set_password"),
    path('verify-password-reset-otp/<uuid:id>/',views.verify_password_reset_otp,name="verify_otp_code"),
    path('accounts/verification-error/', views.otp_verification_error, name="otp_verification_error"),
    path('forgot-password-email/',views.check_forgot_password_email,name="check_forgot_password_email"),
    path("forgot-password/set-new/<uuid:id>/",views.set_forgot_password,name="set_forgot_password")
]