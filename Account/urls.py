from django.urls import path
from . import views

urlpatterns = [
    path('account/register/', views.registeruser, name='register'),
    path('account/login/', views.loginuser, name='login'),
    path('account/forgot-password/', views.forgotpassword, name='forgot_password'),
]