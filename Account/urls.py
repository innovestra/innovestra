from django.urls import path
from . import views

urlpatterns = [
    path('account/register/', views.registeruser, name='register'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('resend-code/', views.resend_verification_code, name='resend_code'),
    path('account/login/', views.loginuser, name='login'),
    path('account/logout/', views.logoutuser, name='logout'),
    path('account/forgot-password/', views.forgotpassword, name='forgot_password'),
    path('password-reset-success/', views.password_reset_success, name='password_reset_success'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
]