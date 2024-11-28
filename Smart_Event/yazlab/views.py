from django.shortcuts import render

# Create your views here.

def login_view(request):
    return render(request, 'yazlab/login.html')

def register_view(request):
    return render(request, 'yazlab/register.html')

def login_view(request):
    return render(request, 'yazlab/home_page.html')

def register_view(request):
    return render(request, 'yazlab/forgot_password.html')
