from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver 
import datetime

# Model untuk alamat pengiriman
class ShippingAddress(models.Model):
    # Relasi dengan pengguna (ForeignKey)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=255)  # Nama lengkap untuk pengiriman
    shipping_email = models.CharField(max_length=255)  # Email untuk pengiriman
    shipping_address = models.TextField()  # Alamat lengkap
    shipping_city = models.CharField(max_length=255)  # Kota
    shipping_zipcode = models.CharField(max_length=255, null=True, blank=True)  # Kode pos (opsional)

    class Meta:
        # Mencegah pluralisasi nama model di admin
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        # Representasi string dari objek alamat pengiriman
        return f'Shipping Address - {str(self.user.id)}. {self.user.username}'

# Fungsi untuk membuat alamat pengiriman default saat pengguna mendaftar
def create_shipping(sender, instance, created, **kwargs):
    if created:  # Jika pengguna baru dibuat
        user_shipping = ShippingAddress(user=instance)  # Buat alamat pengiriman default
        user_shipping.save()  # Simpan ke database

# Menghubungkan sinyal post_save ke fungsi create_shipping
post_save.connect(create_shipping, sender=User)


# Model untuk pesanan
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Relasi dengan pengguna
    full_name = models.CharField(max_length=250)  # Nama lengkap untuk pesanan
    email = models.EmailField(max_length=250)  # Email untuk pesanan
    shipping_address = models.TextField()  # Alamat pengiriman
    amount_paid = models.DecimalField(max_digits=7, decimal_places=0)  # Total pembayaran
    date_ordered = models.DateTimeField(auto_now_add=True)  # Tanggal pesanan dibuat
    shipped = models.BooleanField(default=False)  # Status pengiriman
    date_shipped = models.DateTimeField(blank=True, null=True)  # Tanggal pengiriman selesai (opsional)

    def __str__(self):
        # Representasi string dari objek pesanan
        return f'Order - {str(self.id)}. {self.user}'

# Fungsi untuk mengatur tanggal pengiriman saat status pesanan diubah
@receiver(pre_save, sender=Order)
def set_shipped_date_on_update(sender, instance, **kwargs):
    if instance.pk:  # Jika objek sudah ada di database
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        # Jika status berubah menjadi terkirim, atur tanggal pengiriman
        if instance.shipped and not obj.shipped:
            instance.date_shipped = now


# Model untuk item pesanan
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)  # Relasi dengan pesanan
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)  # Relasi dengan produk
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Relasi dengan pengguna
    quantity = models.PositiveBigIntegerField(default=1)  # Kuantitas item
    price = models.DecimalField(max_digits=7, decimal_places=0)  # Harga item

    def __str__(self):
        # Representasi string dari objek item pesanan
        return f'Order Item - {str(self.id)}. {self.user}'


# Model untuk informasi pembayaran
class PaymentInfo(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),  # Menunggu pembayaran
        ('completed', 'Completed'),  # Pembayaran selesai
        ('failed', 'Failed'),  # Pembayaran gagal
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Relasi dengan pengguna
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='payment')  # Relasi satu ke satu dengan pesanan
    card_name = models.CharField(max_length=255)  # Nama pada kartu
    card_number = models.CharField(max_length=16)  # Nomor kartu (16 digit)
    card_cvv = models.CharField(max_length=4)  # CVV kartu (3 atau 4 digit)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # Status pembayaran
    created_at = models.DateTimeField(auto_now_add=True)  # Tanggal pembuatan

    class Meta:
        # Mencegah pluralisasi nama model di admin
        verbose_name_plural = "Payment Information"

    def __str__(self):
        # Representasi string dari objek informasi pembayaran
        return f'PaymentInfo - {str(self.id)}. {self.user.username}'
