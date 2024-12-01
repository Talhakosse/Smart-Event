from django import forms
from .models import Kullanici
from .models import Etkinlik
from django.contrib.auth.hashers import make_password

class KullaniciForm(forms.ModelForm):

    class Meta:
        model = Kullanici
        fields = ['kullanici_adi', 'password', 'email', 'ad', 'soyad', 'dogum_tarihi', 'cinsiyet', 'ilgi_alanlari', 'telefon_no', 'profil_fotografi']
    
class EtkinlikForm(forms.ModelForm):
    class Meta:
        model = Etkinlik
        fields = ['ad', 'kategori', 'tarih', 'aciklama']