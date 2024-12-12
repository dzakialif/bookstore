from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .models import Product

# Create your views here.
def home(request):
    products = Product.objects.all()
    context = {
        'page_title': 'Book Store',
        'products': products,
    }
    return render(request, 'store/home.html', context)

def about(request):
    context = {'page_title': 'About Us'}
    return render(request, 'store/about.html', context)

def login_user(request):
    context = {'page_title': 'Login Page'}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
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