from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterForm, UpdateUserForm, ChangePasswordForm, UserInfoForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

import json
from cart.cart import Cart

from .models import Product, Category, Profile

# Create your views here.
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()  # Ambil semua kategori
    context = {
        'page_title': 'Book Store',
        'products': products,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)

def product(request, pk):
    products = Product.objects.get(id=pk)
    context = {
        'page_title': 'Book Store',
        'products': products,
    }
    return render(request, 'store/product.html', context)


def category(request, slug):
    print(f'Searching for category with slug: {slug}')  # Log slug yang diminta

    try:
        category = Category.objects.get(slug=slug)
        print(f'Category found: {category.name}')  # Log kategori yang ditemukan

        products = Product.objects.filter(category=category)
        print(f'Found {products.count()} products for this category')  # Log jumlah produk
        
        categories = Category.objects.all()

        context = {
            'page_title': 'Category Page',
            'category': category,
            'categories': categories,
            'products': products,
        }
        return render(request, 'store/category.html', context)

    except Category.DoesNotExist:
        print(f'Category with slug "{slug}" not found.')  # Log jika kategori tidak ditemukan
        messages.error(request, "The Category Doesn't Exist")
        return redirect('store:home')
    

def about(request):
    categories = Category.objects.all()
    context = {
        'page_title': 'About Us',
        'categories': categories,
    }
    return render(request, 'store/about.html', context)


def update_info(request):
    if request.user.is_authenticated:
        # Get Current User
        current_user = Profile.objects.get(user__id=request.user.id)
		# Get Current User's Shipping Info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        
        # get original user form
        user_info = UserInfoForm(request.POST or None, instance=current_user)
        # get user shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        context = {
        'page_title': 'Update Profile',
        'user_info': user_info,
        'shipping_form': shipping_form,
        }
    
        if user_info.is_valid() or shipping_form.is_valid():
			# Save original form
            user_info.save()
			# Save shipping form
            shipping_form.save()
            
            messages.success(request, 'User info has been Updated...')
            return redirect('store:home')
        return render(request, 'store/update_info.html', context)
    else:
        messages.success(request, 'You must be logged in...')
        return redirect('store:home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        
        # Handle form submission (POST request)
        if request.method == 'POST':
            form = ChangePasswordForm(user=current_user, data=request.POST)  # Pass user to form
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)  # Keep user logged in after password change
                messages.success(request, 'Your password was successfully updated!')
                return redirect('store:update_user')  # Redirect to profile or success page
            else:
                messages.error(request, 'Please correct the errors below.')

        # Handle GET request (when the page is initially loaded)
        else:
            form = ChangePasswordForm(user=current_user)  # Pass user to form

        context = {
            'page_title': 'Update Password',
            'forms': form,
        }
        return render(request, 'store/update_password.html', context)
        
    else:
        messages.error(request, 'You must be logged in to update your password.')
        return redirect('store:home')  # Redirect to the home page if not logged in
        
        

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
            
            login(request, current_user)
            messages.success(request, 'User has been Updated...')
            return redirect('store:home')
        return render(request, 'store/update_user.html', context)
    else:
        messages.success(request, 'You must be logged in...')
        return redirect('store:home')  


def login_user(request):
    context = {'page_title': 'Login Page'}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            # get their saved cart from database
            saved_cart = current_user.old_cart
			# Convert database string to python dictionary
            if saved_cart:
				# Convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)
				# Add the loaded cart dictionary to our session
				# Get the cart
                cart = Cart(request)
				# Loop thru the cart and add the items from the database
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            
            messages.success(request, ('You have been Logged in!!'))
            return redirect('store:home')
        else:
            messages.success(request, ('Error!!! Please Try Again!'))
            return redirect('store:login')
        
    else:        
        return render(request, 'store/login.html', context)

def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out...'))
    return redirect('store:home')

def register_user(request):
    register_form = RegisterForm()
    context = {
        'page_title': 'Register',
        'register_form': register_form,
    }
    
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, ('You have registerd successfully...'))
            return redirect('store:login')
        else:
            messages.success(request, ('Oopss!! There was a problem... Please Try Again!!'))
            return redirect('store:register')
    else:
        return render(request, 'store/register.html', context)
    
    