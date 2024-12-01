from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import KullaniciForm
from .models import Kullanici
from .models import Etkinlik
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Kullanici, Etkinlik
from django.contrib.auth.hashers import make_password
from django.db.models import Q
# Kullanıcı Girişi
def login_view(request):
    if request.method == "POST":
        kullanici_adi = request.POST.get("kullanici_adi")
        sifre = request.POST.get("sifre")
        user = authenticate(request, username=kullanici_adi, password=sifre)
        if user is not None:
            login(request, user)
            return redirect('home_page')
        else:
            messages.error(request, "Kullanıcı adı veya şifre hatalı.")
    return render(request, 'yazlab/login.html')

# Kullanıcı Kaydı
def register_view(request):
    if request.method == "POST":
        kullanici_adi = request.POST.get("kullanici_adi")
        sifre = request.POST.get("sifre")
        eposta = request.POST.get("eposta")
        ad = request.POST.get("ad")
        soyad = request.POST.get("soyad")
        dogum_tarihi = request.POST.get("dogum_tarihi")
        cinsiyet = request.POST.get("cinsiyet")
        ilgi_alanlari = request.POST.get("ilgi_alanlari")  # Serbest metin olarak alınıyor

        kullanici = Kullanici.objects.create(
            kullanici_adi=kullanici_adi,
            password=make_password(sifre),
            eposta=eposta,
            ad=ad,
            soyad=soyad,
            dogum_tarihi=dogum_tarihi,
            cinsiyet=cinsiyet,
            ilgi_alanlari=ilgi_alanlari  # İlgi alanlarını kaydediyoruz
        )
        kullanici.save()
        return redirect('login')

    return render(request, 'yazlab/register.html')

@login_required
@login_required
def home_page_view(request):
    # Giriş yapan kullanıcı
    kullanici = request.user

    # Kullanıcının ilgi alanlarını analiz et
    if kullanici.ilgi_alanlari:
        ilgi_alanlari = [kelime.strip().lower() for kelime in kullanici.ilgi_alanlari.split(",")]  # Virgülle ayrılmışsa
        
        # İlgi alanlarına uygun etkinlikleri filtrele
        q_objects = Q()  # Boş bir Q nesnesi oluştur
        for kelime in ilgi_alanlari:
            q_objects |= Q(kategori__icontains=kelime) | Q(aciklama__icontains=kelime)
        
        # Tüm eşleşen etkinlikleri al
        etkinlikler = Etkinlik.objects.filter(q_objects).distinct()
    else:
        etkinlikler = Etkinlik.objects.none()  # Eğer ilgi alanı yoksa boş liste döndür

    # Etkinlikleri şablona gönder
    return render(request, 'yazlab/home_page.html', {
        'etkinlikler': etkinlikler,
    })
# Profil Güncelleme (Opsiyonel)
@login_required
def profil_guncelle_view(request):
    if request.method == "POST":
        ilgi_alani_listesi = request.POST.getlist('ilgi_alanlari')
        kullanici = request.user.profil
        kullanici.ilgi_alanlari.clear()
        for ilgi in ilgi_alani_listesi:
            ilgi_alani_obj = IlgiAlani.objects.get(ad=ilgi)
            kullanici.ilgi_alanlari.add(ilgi_alani_obj)
        kullanici.save()
        return redirect('home_page')

    ilgi_alanlari = IlgiAlani.objects.all()
    return render(request, 'yazlab/profil_guncelle.html', {"ilgi_alanlari": ilgi_alanlari})



def forgot_pass_view(request):
    return render(request, 'yazlab/forgot_pass.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Başarıyla çıkış yaptınız.')
    return redirect('login')
