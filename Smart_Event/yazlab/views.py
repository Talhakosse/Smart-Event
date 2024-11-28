from django.shortcuts import render

# Create your views here.

def login_view(request):
    return render(request, 'yazlab/login.html')

def register_view(request):
    return render(request, 'yazlab/register.html')

def home_page_view(request):
    return render(request, 'yazlab/home_page.html')

def forgot_pass_view(request):
    return render(request, 'yazlab/forgot_pass.html')
