from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import KullaniciForm
from .models import Kullanici
from django.contrib.auth.decorators import login_required
# Create your views here.

def login_view(request):
    if request.method == 'POST':
        kullanici_adi = request.POST.get('kullanici_adi')
        sifre = request.POST.get('sifre')

        # Kullanıcıyı doğrula
        try:
            kullanici = Kullanici.objects.get(kullanici_adi=kullanici_adi, sifre=sifre)
            # Doğrulama başarılı
            # messages.success(request, f'Hoş geldiniz, {kullanici.ad}!')
            return redirect('home_page')  # Giriş başarılıysa yönlendir
        except Kullanici.DoesNotExist:
            # Kullanıcı bulunamadı
            messages.error(request, 'Geçersiz kullanıcı adı veya şifre.')


    return render(request, 'yazlab/login.html')


@login_required
def home_page_view(request):
    return render(request, 'yazlab/home_page.html', {'user': request.user})

def forgot_pass_view(request):
    return render(request, 'yazlab/forgot_pass.html')

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

def logout_view(request):
    logout(request)
    messages.success(request, 'Başarıyla çıkış yaptınız.')
    return redirect('login')
