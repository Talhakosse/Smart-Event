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
from .forms import EtkinlikForm

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
        email = request.POST.get("email")
        ad = request.POST.get("ad")
        soyad = request.POST.get("soyad")
        dogum_tarihi = request.POST.get("dogum_tarihi")
        cinsiyet = request.POST.get("cinsiyet")
        ilgi_alanlari = request.POST.get("ilgi_alanlari")  # Serbest metin olarak alınıyor
        telefon_no =  request.POST.get("telefon_no") 
        konum = request.POST.get("konum")
        profil_fotografi = request.FILES.get("profil_fotografi")

        # Kullanıcı adı ve e-posta duplicate kontrolü
        if Kullanici.objects.filter(kullanici_adi=kullanici_adi).exists():
            messages.error(request, "Bu kullanıcı adı zaten kayıtlı.")
            return render(request, 'yazlab/register.html', {
                'kullanici_adi': kullanici_adi,
                'email': email,
                'ad': ad,
                'soyad': soyad,
                'dogum_tarihi': dogum_tarihi,
                'cinsiyet': cinsiyet,
                'ilgi_alanlari': ilgi_alanlari,
                'telefon_no': telefon_no,
                'konum': konum,
            })

        if Kullanici.objects.filter(email=email).exists():
            messages.error(request, "Bu e-posta adresi zaten kayıtlı.")
            return render(request, 'yazlab/register.html', {
                'kullanici_adi': kullanici_adi,
                'email': email,
                'ad': ad,
                'soyad': soyad,
                'dogum_tarihi': dogum_tarihi,
                'cinsiyet': cinsiyet,
                'ilgi_alanlari': ilgi_alanlari,
                'telefon_no': telefon_no,
                'konum': konum,
            })

        # Kullanıcı oluşturma
        kullanici = Kullanici.objects.create(
            kullanici_adi=kullanici_adi,
            password=make_password(sifre),
            email=email,
            ad=ad,
            soyad=soyad,
            dogum_tarihi=dogum_tarihi,
            cinsiyet=cinsiyet,
            ilgi_alanlari=ilgi_alanlari,
            telefon_no=telefon_no,  # Telefon numarası kaydediliyor
            konum=konum,  # Konum kaydediliyor
            profil_fotografi=profil_fotografi  # İlgi alanlarını kaydediyoruz
        )
        kullanici.save()

        messages.success(request, "Kayıt başarıyla oluşturuldu. Giriş yapabilirsiniz.")
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

def logout_view(request):
    logout(request)
    messages.success(request, 'Başarıyla çıkış yaptınız.')
    return redirect('login')

@login_required
def create_event_view(request):
    if request.method == 'POST':
        form = EtkinlikForm(request.POST)
        if form.is_valid():
            etkinlik = form.save(commit=False)
            etkinlik.created_by = request.user  # Etkinliği oluşturan kullanıcıyı kaydet
            etkinlik.save()
            return redirect('home_page')  # Etkinlik oluşturulduktan sonra ana sayfaya yönlendirme
    else:
        form = EtkinlikForm()
    return render(request, 'yazlab/create_event.html', {'form': form})

from django.contrib.auth.views import PasswordResetView
from django.contrib import messages
from django.urls import reverse_lazy

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'

    def form_valid(self, form):
        # Her durumda kullanıcıya genel bir mesaj göster
        messages.info(self.request, "Eğer bu e-posta adresi sistemde kayıtlıysa, şifre sıfırlama bağlantısı gönderilecektir.")
        return super().form_valid(form)
