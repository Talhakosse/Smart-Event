from django import forms
from .models import Kullanici
from django.contrib.auth.hashers import make_password

class KullaniciForm(forms.ModelForm):

    class Meta:
        model = Kullanici
        fields = ['kullanici_adi', 'password', 'eposta', 'ad', 'soyad', 'dogum_tarihi', 'cinsiyet', 'ilgi_alanlari']
    
