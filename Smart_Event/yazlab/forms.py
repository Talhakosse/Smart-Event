from django import forms
from .models import Kullanici
from django.contrib.auth.hashers import make_password

class KullaniciForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput, 
        label="Şifre",
        min_length=8  # Şifre uzunluğunu kontrol etmek için
    )

    class Meta:
        model = Kullanici
        fields = ['kullanici_adi', 'password', 'eposta', 'ad', 'soyad', 'dogum_tarihi', 'cinsiyet', 'ilgi_alanlari']

    def clean_eposta(self):
        eposta = self.cleaned_data.get('eposta')
        if Kullanici.objects.filter(eposta=eposta).exists():
            raise forms.ValidationError("Bu e-posta daha önce kaydedilmiş.")
        return eposta

    
