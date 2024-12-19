from django.db import models
from django.utils.text import slugify
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Model untuk profil pengguna
class Profile(models.Model):
    # Relasi one-to-one dengan model User bawaan Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)  # Waktu terakhir profil diubah
    phone = models.CharField(max_length=20, blank=True)  # Nomor telepon pengguna (opsional)
    address = models.CharField(max_length=200, blank=True)  # Alamat pengguna (opsional)
    city = models.CharField(max_length=200, blank=True)  # Kota pengguna (opsional)
    zipcode = models.CharField(max_length=200, blank=True)  # Kode pos pengguna (opsional)
    old_cart = models.CharField(max_length=200, blank=True, null=True)  # Data keranjang belanja lama (opsional)

    def __str__(self):
        # Representasi string dari objek profil
        return self.user.username

# Sinyal untuk membuat profil secara otomatis ketika pengguna baru dibuat
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:  # Jika pengguna baru dibuat
        user_profile = Profile(user=instance)  # Buat objek profil untuk pengguna tersebut
        user_profile.save()  # Simpan profil ke database

# Menghubungkan sinyal post_save dengan fungsi create_profile
post_save.connect(create_profile, sender=User)

# Model untuk kategori produk
class Category(models.Model):
    name = models.CharField(max_length=50)  # Nama kategori
    slug = models.SlugField(blank=True, editable=False, unique=True)  # Slug untuk URL (dibuat otomatis)

    class Meta:
        # Menentukan nama jamak di admin panel
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        # Membuat slug secara otomatis berdasarkan nama kategori jika belum ada
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)  # Panggil metode save bawaan

    def __str__(self):
        # Representasi string dari objek kategori
        return self.name

# Model untuk produk
class Product(models.Model):
    name = models.CharField(max_length=100)  # Nama produk
    price = models.DecimalField(max_digits=7, decimal_places=0)  # Harga produk
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)  # Relasi dengan kategori produk
    description = models.TextField(default='', blank=True, null=True)  # Deskripsi produk (opsional)
    image = models.ImageField(upload_to='uploads/product/')  # Gambar produk (diunggah ke folder tertentu)

    def __str__(self):
        # Representasi string dari objek produk
        return self.name
