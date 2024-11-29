from django.contrib import admin
from .models import Kullanici

@admin.register(Kullanici)
class KullaniciAdmin(admin.ModelAdmin):
    list_display = ('kullanici_adi', 'eposta', 'ad', 'soyad', 'dogum_tarihi')
