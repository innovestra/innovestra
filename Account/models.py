from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from datetime import timedelta
import random
import string
# Create your models here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Empty username field to satisfy AbstractBaseUser requirements
    username = models.CharField(max_length=150, unique=True, null=True)
    email = models.EmailField(unique=True, verbose_name="email address")
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    is_staff = models.BooleanField(default=False, help_text="Designates whether the user is a staff member")
    is_active = models.BooleanField(default=True, help_text="Designates whether the user is active in the system")
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now_add=True)
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
    def __str__(self):
        return self.first_name + " " + self.last_name
    

class PendingRegistration(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=255)
    verification_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.verification_code:
            self.verification_code = ''.join(random.choices(string.digits, k=6))
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def time_remaining(self):
        if self.is_expired():
            return 0
        delta = self.expires_at - timezone.now()
        return int(delta.total_seconds())
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.email} - {self.verification_code}"
    

class PasswordReset(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reset_token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.reset_token:
            self.reset_token = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=1)  # Token expires in 1 hour
        super().save(*args, **kwargs)
    
    def is_expired(self):
        return timezone.now() > self.expires_at or self.is_used
    
    def __str__(self):
        return f"Password reset for {self.user.email}"
    
    class Meta:
        ordering = ['-created_at']