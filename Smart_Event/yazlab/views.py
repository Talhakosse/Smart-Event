from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import KullaniciForm

# Create your views here.

def login_view(request):
    return render(request, 'yazlab/login.html')

# def register_view(request):
#     return render(request, 'yazlab/register.html')

def home_page_view(request):
    return render(request, 'yazlab/home_page.html')

def forgot_pass_view(request):
    return render(request, 'yazlab/forgot_pass  .html')

def register_view(request):
    if request.method == 'POST':
        form = KullaniciForm(request.POST, request.FILES)  # Dosyaları da alıyoruz
        if form.is_valid():
            form.save()  # Bilgileri veritabanına kaydet
            messages.success(request, 'Kayıt başarılı! Giriş yapabilirsiniz.')
            return redirect('login')  # Giriş sayfasına yönlendirme
        else:
            messages.error(request, 'Kayıt sırasında bir hata oluştu. Lütfen bilgilerinizi kontrol edin.')
    else:
        form = KullaniciForm()
    
    return render(request, 'yazlab/register.html', {'form': form})