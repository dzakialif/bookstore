from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterForm, UpdateUserForm, ChangePasswordForm, UserInfoForm

from django.views.generic import ListView, TemplateView, DetailView

from payment.forms import ShippingForm
from payment.models import ShippingAddress

import json
from cart.cart import Cart

from .models import Product, Category, Profile

# Buat view untuk halaman utama
class HomeView(ListView):
    model = Product  # Model yang digunakan
    template_name = 'store/home.html'  # Template untuk halaman utama
    context_object_name = 'products'  # Nama variabel di template

    def get_context_data(self, **kwargs):
        # Tambahkan konteks tambahan
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Book Store'  # Judul halaman
        context['categories'] = Category.objects.all()  # Ambil semua kategori
        return context 

# Detail produk
class ProductDetailView(DetailView):
    model = Product  # Model yang digunakan
    template_name = 'store/product.html'  # Template untuk halaman detail produk
    context_object_name = 'products'  # Nama variabel di template

    def get_context_data(self, **kwargs):
        # Tambahkan konteks tambahan
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Book Store'  # Judul halaman
        return context

# Halaman kategori produk berdasarkan slug
def category(request, slug):
    try:
        category = Category.objects.get(slug=slug)  # Ambil kategori berdasarkan slug
        products = Product.objects.filter(category=category)  # Ambil produk yang sesuai
        categories = Category.objects.all()  # Ambil semua kategori

        context = {
            'page_title': 'Category Page',
            'category': category,
            'categories': categories,
            'products': products,
        }
        return render(request, 'store/category.html', context)
    except Category.DoesNotExist:
        # Jika kategori tidak ditemukan
        messages.error(request, "The Category Doesn't Exist")
        return redirect('store:home')

# Halaman tentang
class AboutView(TemplateView):
    template_name = 'store/about.html'  # Template untuk halaman tentang

    def get_context_data(self, **kwargs):
        # Tambahkan konteks tambahan
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'About Us'  # Judul halaman
        context['categories'] = Category.objects.all()  # Ambil semua kategori
        return context

# Perbarui informasi pengguna
def update_info(request):
    if request.user.is_authenticated:
        # Ambil profil dan alamat pengiriman pengguna saat ini
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        
        # Form untuk memperbarui informasi pengguna dan alamat pengiriman
        user_info = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        
        context = {
            'page_title': 'Update Profile',
            'user_info': user_info,
            'shipping_form': shipping_form,
        }
        
        # Tangani pengiriman form
        if request.method == 'POST':
            if user_info.is_valid() and shipping_form.is_valid():
                # Simpan perubahan
                user_info.save()
                shipping_form.save()
                messages.success(request, 'User info has been updated successfully.')
                return redirect('store:home')
            else:
                messages.error(request, 'Oops! There was a problem. Please check the form and try again.')
        
        return render(request, 'store/update_info.html', context)
    else:
        messages.error(request, 'You must be logged in to update your information.')
        return redirect('store:home')

# Perbarui kata sandi
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        
        if request.method == 'POST':
            form = ChangePasswordForm(user=current_user, data=request.POST)
            if form.is_valid():
                form.save()  # Simpan kata sandi baru
                update_session_auth_hash(request, form.user)  # Jaga agar pengguna tetap login
                messages.success(request, 'Your password was successfully updated!')
                return redirect('store:update_user')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = ChangePasswordForm(user=current_user)
        
        context = {
            'page_title': 'Update Password',
            'forms': form,
        }
        return render(request, 'store/update_password.html', context)
    else:
        messages.error(request, 'You must be logged in to update your password.')
        return redirect('store:home')

# Perbarui data pengguna
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        context = {
            'page_title': 'Update Profile',
            'user_form': user_form
        }
    
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)  # Perbarui sesi pengguna
            messages.success(request, 'User has been Updated...')
            return redirect('store:home')
        return render(request, 'store/update_user.html', context)
    else:
        messages.success(request, 'You must be logged in...')
        return redirect('store:home')

# Login pengguna
def login_user(request):
    context = {'page_title': 'Login Page'}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Sinkronkan keranjang lama dari database
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            
            messages.success(request, 'You have been Logged in!!')
            return redirect('store:home')
        else:
            messages.error(request, 'Error!!! Please Try Again!')
            return redirect('store:login')
    else:        
        return render(request, 'store/login.html', context)

# Logout pengguna
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out...')
    return redirect('store:home')

# Registrasi pengguna baru
def register_user(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()  # Simpan pengguna baru
            messages.success(request, 'You have registered successfully...')
            return redirect('store:login')
        else:
            messages.error(request, 'Oopss!! There was a problem... Please Try Again!!')
    else:
        register_form = RegisterForm()
    
    context = {
        'page_title': 'Register',
        'register_form': register_form,
    }
    return render(request, 'store/register.html', context)
