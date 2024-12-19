import datetime
from django.contrib import messages
from django.shortcuts import redirect, render
from cart.cart import Cart
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ShippingForm, PaymentForm
from .models import ShippingAddress, Order, OrderItem, PaymentInfo
from store.models import Profile

# Fungsi untuk memeriksa apakah pengguna adalah admin atau superuser
def is_staff_admin(user):
    """
    Periksa apakah pengguna ada di grup 'staff_admin' atau merupakan superuser.
    """
    return user.groups.filter(name='staff_admin').exists()

# View untuk menampilkan detail pesanan
class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'payment/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        # Hanya tampilkan pesanan yang dimiliki oleh pengguna yang login
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Tambahkan item pesanan dan informasi pembayaran ke konteks
        context['items'] = self.object.orderitem_set.all()
        context['payment'] = getattr(self.object, 'payment', None)  # Ambil informasi pembayaran
        return context

    def handle_no_permission(self):
        # Arahkan pengguna yang tidak berizin ke halaman login
        messages.error(self.request, "You must be logged in to view your order details.")
        return redirect('store:login')

# View untuk menampilkan riwayat pesanan pengguna
class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'payment/order_history.html'
    context_object_name = 'orders'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Order History'
        return context

    def get_queryset(self):
        # Hanya tampilkan pesanan milik pengguna yang login, urutkan berdasarkan tanggal
        return super().get_queryset().filter(user=self.request.user).order_by('-date_ordered')

    def handle_no_permission(self):
        # Arahkan pengguna yang tidak berizin ke halaman login
        messages.error(self.request, "You must be logged in to view your order history.")
        return redirect('store:login')

# View untuk menampilkan dan memperbarui detail pembayaran
def payment_detail(request, pk):
    if request.user.is_authenticated:
        # Ambil informasi pembayaran berdasarkan ID
        payment = PaymentInfo.objects.get(id=pk)

        # Periksa apakah pengguna memiliki akses ke pembayaran ini
        if payment.user != request.user and not (is_staff_admin(request.user) or request.user.is_superuser):
            messages.error(request, "You do not have permission to view this payment.")
            return redirect('store:home')

        # Tangani perubahan status pembayaran melalui POST
        if request.method == 'POST':
            new_status = request.POST.get('status')
            if new_status in dict(PaymentInfo.STATUS_CHOICES):  # Validasi status yang dipilih
                payment.status = new_status
                payment.save()
                messages.success(request, "Payment status updated successfully!")
            else:
                messages.error(request, "Invalid status selected.")
            return redirect('payment:payment_detail', pk=pk)

        # Render halaman detail pembayaran
        context = {
            'page_title': 'Payment Detail',
            'payment': payment,
        }
        return render(request, 'payment/payment_detail.html', context)
    else:
        messages.error(request, "You must be logged in to view payment details.")
        return redirect('store:login')

# View untuk dashboard pembayaran (hanya untuk admin)
def payment_dashboard(request):
    if request.user.is_authenticated and (is_staff_admin(request.user) or request.user.is_superuser):
        # Ambil semua informasi pembayaran
        payments = PaymentInfo.objects.all().order_by('-created_at')

        # Render halaman dashboard pembayaran
        context = {
            'page_title': 'Payment Dashboard',
            'payments': payments,
        }
        return render(request, 'payment/payment_dashboard.html', context)
    else:
        messages.error(request, "Access Denied. You do not have permission to view this page.")
        return redirect('store:home')

# View untuk mengelola pesanan individual (hanya untuk admin)
def orders(request, pk):
    if request.user.is_authenticated and (is_staff_admin(request.user) or request.user.is_superuser):
        order = Order.objects.get(id=pk)  # Ambil pesanan berdasarkan ID
        items = OrderItem.objects.filter(order=pk)  # Ambil item yang terkait dengan pesanan

        if request.POST:
            status = request.POST['shipping_status']
            if status == "true":
                order = Order.objects.filter(id=pk)
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                order = Order.objects.filter(id=pk)
                order.update(shipped=False)
            messages.success(request, "Shipping Status Updated")
            return redirect('store:home')

        return render(request, 'payment/orders.html', {"order": order, "items": items})
    else:
        messages.success(request, "Access Denied")
        return redirect('store:home')

# View untuk menampilkan pesanan yang belum dikirim (hanya untuk admin)
def not_shipped_dash(request):
    if request.user.is_authenticated and (is_staff_admin(request.user) or request.user.is_superuser):
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            now = datetime.datetime.now()
            order.update(shipped=True, date_shipped=now)
            messages.success(request, "Shipping Status Updated")
            return redirect('store:home')

        return render(request, "payment/not_shipped_dash.html", {
            'page_title': 'Un-shipped Dashboard',
            'orders': orders
        })
    else:
        messages.success(request, "Access Denied")
        return redirect('store:home')

# View untuk pesanan yang sudah dikirim (hanya untuk admin)
def shipped_dash(request):
    if request.user.is_authenticated and (is_staff_admin(request.user) or request.user.is_superuser):
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            now = datetime.datetime.now()
            order.update(shipped=False)
            messages.success(request, "Shipping Status Updated")
            return redirect('store:home')

        return render(request, "payment/shipped_dash.html", {
            'page_title': 'Shipped Dashboard',
            'orders': orders
        })
    else:
        messages.success(request, "Access Denied")
        return redirect('store:home')

# Proses pesanan dan pembayaran
def process_order(request):
    # Logika pemrosesan pesanan
    pass  # Dipersingkat untuk kejelasan
