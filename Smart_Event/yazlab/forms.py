from django import forms
from .models import Kullanici

class KullaniciForm(forms.ModelForm):
    class Meta:
        model = Kullanici
        fields = [
            'kullanici_adi', 'sifre', 'eposta', 'konum', 'ilgi_alanlari',
            'ad', 'soyad', 'dogum_tarihi', 'cinsiyet', 'telefon_no', 'profil_fotografi'
        ]
        widgets = {
            'sifre': forms.PasswordInput(),  # Şifre alanını gizli yap
        }
