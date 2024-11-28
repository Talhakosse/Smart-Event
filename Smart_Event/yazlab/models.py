from django.db import models

# Create your models here.

class OrnekModel(models.Model):
    isim = models.CharField(max_length=100)
    yas = models.IntegerField()

    def __str__(self):
        return self.isim
