from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from store.models import Product
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.
def is_staff_admin(user):
    return user.groups.filter(name='staff_admin').exists()

def cart_summary(request):
    if is_staff_admin(request.user):  # Pengecekan grup
        messages.error(request, "Staff Admin accounts cannot perform transactions.")
        return redirect('store:home')
    # get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    context = {
        'page_title': 'Cart',
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals,
    }
    return render(request, 'cart/cart_summary.html', context)


def cart_add(request):
    if is_staff_admin(request.user):  # Pengecekan grup
        messages.error(request, "Staff Admin accounts cannot perform transactions.")
        return redirect('store:home')
    # get the cart
    cart = Cart(request)
    # test for post
    if request.POST.get('action') == 'post':
        # get the stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        
        product = get_object_or_404(Product, id=product_id)
        
        # save to session
        cart.add(product=product, quantity=product_qty)
        
        # get cart quantity
        cart_quantity = cart.__len__()
        
        # return response
        # response = JsonResponse({'Product Name: ': product.name})
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, ('Product added to cart...'))
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # get the stuff
        product_id = int(request.POST.get('product_id'))
        
        # call delete function in cart
        cart.delete(product=product_id)
        
        response = JsonResponse({'product':product_id})
        messages.success(request, ('Your remove product...'))
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # get the stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        
        cart.update(product=product_id, quantity=product_qty)
        
        response = JsonResponse({'qty':product_qty})
        messages.success(request, ('Your cart has been updated...'))
        return response
    