from django.db import models

class Kullanici(models.Model):
    kullanici_adi = models.CharField(max_length=150, unique=True)
    sifre = models.CharField(max_length=128)  # Şifreyi hashlemeden saklamak için
    eposta = models.EmailField(unique=True)
    konum = models.CharField(max_length=255, null=True, blank=True)
    ilgi_alanlari = models.TextField(null=True, blank=True)
    ad = models.CharField(max_length=50)
    soyad = models.CharField(max_length=50)
    dogum_tarihi = models.DateField()
    cinsiyet = models.CharField(max_length=10)
    telefon_no = models.CharField(max_length=15, null=True, blank=True)
    profil_fotografi = models.ImageField(upload_to='profil_fotograflari/', null=True, blank=True)

    def __str__(self):
        return self.kullanici_adi
