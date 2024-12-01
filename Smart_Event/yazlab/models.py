from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, kullanici_adi, email, password=None, **extra_fields):
        """
        Normal kullanıcı oluşturma.
        """
        if not email:
            raise ValueError("Kullanıcıların bir e-posta adresi olması gerekiyor.")
        if not kullanici_adi:
            raise ValueError("Kullanıcı adı gereklidir.")

        email = self.normalize_email(email)
        user = self.model(kullanici_adi=kullanici_adi, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, kullanici_adi, email, password=None, **extra_fields):
     extra_fields.setdefault('is_staff', True)
     extra_fields.setdefault('is_superuser', True)

    # Varsayılan bir dogum_tarihi ekleyin veya kontrol edin
     if 'dogum_tarihi' not in extra_fields:
        extra_fields['dogum_tarihi'] = None  # Boş bırakılmasını sağlar

     return self.create_user(kullanici_adi, email, password, **extra_fields)

class Kullanici(AbstractBaseUser, PermissionsMixin):
    kullanici_adi = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    ad = models.CharField(max_length=50)
    soyad = models.CharField(max_length=50)
    dogum_tarihi = models.DateField(null=True, blank=True)
    cinsiyet = models.CharField(max_length=10, null=True, blank=True)
    telefon_no = models.CharField(max_length=15, null=True, blank=True)
    profil_fotografi = models.ImageField(upload_to='profil_fotograflari/', null=True, blank=True)
    ilgi_alanlari = models.TextField(null=True, blank=True)
    konum = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='kullanici_groups',  # Çakışmayı önlemek için related_name ekleniyor
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='kullanici_permissions',  # Çakışmayı önlemek için related_name ekleniyor
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    objects = CustomUserManager()  # Güncellenmiş yöneticiyi burada kullanıyoruz

    USERNAME_FIELD = 'kullanici_adi'
    REQUIRED_FIELDS = ['email', 'ad', 'soyad']

    def __str__(self):
        return self.kullanici_adi

class Etkinlik(models.Model):
    ad = models.CharField(max_length=100)
    kategori = models.CharField(max_length=50)  # Kategori adı: örneğin, "spor", "teknoloji"
    tarih = models.DateField()
    aciklama = models.TextField()
    # created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.ad
