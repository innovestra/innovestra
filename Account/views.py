from django.shortcuts import render

# Create your views here.
def registeruser(request):
    return render(request, 'account/register.html')

def loginuser(request):
    return render(request, 'account/login.html')

def forgotpassword(request):
    return render(request, 'account/forgot_password.html')