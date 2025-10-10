import string
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import PendingRegistration, CustomUser, PasswordReset
from .forms import RegistrationForm, VerificationForm, ForgotPasswordForm, ResetPasswordForm
import json
from datetime import timedelta
import random
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def registeruser(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Delete any existing pending registration for this email
            PendingRegistration.objects.filter(email=form.cleaned_data['email']).delete()
            
            # Create pending registration
            pending = PendingRegistration.objects.create(
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=make_password(form.cleaned_data['password'])
            )
            
            # Send verification email
            try:
                send_mail(
                    subject='Verify Your Innovestra Account',
                    message=f'''
Hello {pending.first_name},

Thank you for registering with Innovestra Tech Enterprises!

Your verification code is: {pending.verification_code}

This code will expire in 10 minutes.

If you didn't create an account, please ignore this email.

Best regards,
Innovestra Team
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[pending.email],
                    fail_silently=False,
                )
                
                # Store email in session for verification page
                request.session['pending_email'] = pending.email
                messages.success(request, 'Verification code sent to your email!')
                return redirect('verify_email')
                
            except Exception as e:
                pending.delete()
                messages.error(request, 'Failed to send verification email. Please try again.')
                return redirect('register')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = RegistrationForm()
    
    return render(request, 'account/register.html', {'form': form})

def verify_email(request):
    email = request.session.get('pending_email')
    
    if not email:
        messages.error(request, 'No pending registration found.')
        return redirect('register')
    
    try:
        pending = PendingRegistration.objects.get(email=email)
        
        # Check if expired
        if pending.is_expired():
            pending.delete()
            del request.session['pending_email']
            messages.error(request, 'Verification code expired. Please register again.')
            return redirect('register')
        
        if request.method == 'POST':
            form = VerificationForm(request.POST)
            if form.is_valid():
                code = form.cleaned_data['code']
                
                if code == pending.verification_code:
                    # Create the user account
                    user = CustomUser.objects.create(
                        username=pending.email.split('@')[0] + str(CustomUser.objects.count()),
                        email=pending.email,
                        first_name=pending.first_name,
                        last_name=pending.last_name,
                        password=pending.password
                    )
                    
                    # Delete pending registration
                    pending.delete()
                    del request.session['pending_email']
                    
                    messages.success(request, 'Account created successfully! Please login.')
                    return redirect('login')
                else:
                    messages.error(request, 'Invalid verification code. Please try again.')
        else:
            form = VerificationForm()
        
        # Calculate time remaining
        time_remaining = pending.time_remaining()
        
        context = {
            'form': form,
            'email': email,
            'time_remaining': time_remaining
        }
        return render(request, 'account/verify_email.html', context)
        
    except PendingRegistration.DoesNotExist:
        del request.session['pending_email']
        messages.error(request, 'Verification session expired. Please register again.')
        return redirect('register')


def resend_verification_code(request):
    email = request.session.get('pending_email')
    
    if not email:
        return redirect('register')
    
    try:
        pending = PendingRegistration.objects.get(email=email)
        
        # Generate new code and extend expiration
        pending.verification_code = ''.join(random.choices(string.digits, k=6))
        pending.expires_at = timezone.now() + timedelta(minutes=10)
        pending.save()
        
        # Send new code
        send_mail(
            subject='Account Verification Code',
            message=f'''
Hello {pending.first_name},

Your new verification code is: {pending.verification_code}

This code will expire in 10 minutes.

Best regards,
Innovestra Team
            ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[pending.email],
            fail_silently=False,
        )
        
        messages.success(request, 'New verification code sent!')
        return redirect('verify_email')
        
    except PendingRegistration.DoesNotExist:
        messages.error(request, 'No pending registration found.')
        return redirect('register')

def loginuser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                # Log the user in
                login(request, user)
                # send user login email notification
                send_mail(
                    subject='New Login Notification',
                    message=f'''
Hello {user.first_name},
We noticed a new login to your Innovestra account.
If this was you, you can safely ignore this email. If you did not log in, please reset your password immediately.
Best regards,
Innovestra Team
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=True,
                )

                messages.success(request, 'You have successfully logged in.')
                return redirect('homepage')  # Redirect to a home page or dashboard
            else:
                messages.error(request, 'Invalid password. Please try again.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'No account found with this email.')
    return render(request, 'account/login.html')

def forgotpassword(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = CustomUser.objects.get(email=email)
            
            # Delete any existing unused reset tokens for this user
            PasswordReset.objects.filter(user=user, is_used=False).delete()
            
            # Create new password reset token
            reset = PasswordReset.objects.create(user=user)
            
            # Build reset link
            reset_link = request.build_absolute_uri(
                reverse('reset_password', kwargs={'token': reset.reset_token})
            )
            
            # Send email
            try:
                send_mail(
                    subject='Password Reset Request',
                    message=f'''
Hello {user.first_name},

We received a request to reset your password for your Innovestra account.

Click the link below to reset your password:
{reset_link}

This link will expire in 1 hour.

If you didn't request a password reset, please ignore this email or contact support if you have concerns.

Best regards,
Innovestra Team
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                
                messages.success(request, 'Password reset link sent to your email!')
                return redirect('password_reset_success')
                
            except Exception as e:
                reset.delete()
                messages.error(request, f'Failed to send reset email: {str(e)}')
                return redirect('forgot_password')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'account/forgot_password.html', {'form': form})


def password_reset_success(request):
    return render(request, 'account/password_reset_success.html')


def reset_password(request, token):
    try:
        reset = PasswordReset.objects.get(reset_token=token)
        
        # Check if token is expired or used
        if reset.is_expired():
            messages.error(request, 'This password reset link has expired or been used.')
            return redirect('forgot_password')
        
        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                # Update user password
                user = reset.user
                user.password = make_password(form.cleaned_data['new_password1'])
                user.save()
                
                # Mark token as used
                reset.is_used = True
                reset.save()
                # sucessful password reset email notification
                send_mail(
                    subject='Password Successfully Reset',
                    message=f'''
Hello {user.first_name},
Your password has been successfully reset. If you did not perform this action, please contact our support team immediately.
Best regards,
Innovestra Team
Website: {settings.SITE_URL}                   ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=True,
                )
                messages.success(request, 'Password reset successful! You can now login with your new password.')
                return redirect('login')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{error}')
        else:
            form = ResetPasswordForm()
        
        context = {
            'form': form,
            'token': token
        }
        return render(request, 'account/reset_password.html', context)
        
    except PasswordReset.DoesNotExist:
        messages.error(request, 'Invalid password reset link.')
        return redirect('forgot_password')

def logoutuser(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('login')