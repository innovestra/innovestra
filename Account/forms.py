from django import forms
from .models import CustomUser

class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirm Password")
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password and password2 and password != password2:
            raise forms.ValidationError('Passwords do not match.')
        
        return cleaned_data


class VerificationForm(forms.Form):
    code = forms.CharField(max_length=6, min_length=6, required=True,
                          widget=forms.TextInput(attrs={
                              'placeholder': '000000',
                              'class': 'form-control form-control-lg text-center',
                              'maxlength': '6'
                          }))
    

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'example@gmail.com'
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('No account found with this email address.')
        return email


class ResetPasswordForm(forms.Form):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg border-end-0',
            'placeholder': 'Enter new password'
        }),
        required=True,
        label="New Password"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg border-end-0',
            'placeholder': 'Confirm new password'
        }),
        required=True,
        label="Confirm New Password"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')
        
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Passwords do not match.')
            
            if len(password1) < 8:
                raise forms.ValidationError('Password must be at least 8 characters long.')
        
        return cleaned_data