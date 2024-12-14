import datetime
from django.contrib import messages
from django.shortcuts import redirect, render
from cart.cart import Cart
from .forms import ShippingForm, PaymentForm
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

# Create your views here.

def orders(request, pk):
	if request.user.is_authenticated and request.user.is_superuser:
		# Get the order
		order = Order.objects.get(id=pk)
		# Get the order items
		items = OrderItem.objects.filter(order=pk)
  
		return render(request, 'payment/orders.html', {"order":order, "items":items})
    

def not_shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=False)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# Get the order
			order = Order.objects.filter(id=num)
			# grab Date and time
			now = datetime.datetime.now()
			# update order
			order.update(shipped=True, date_shipped=now)
			# redirect
			messages.success(request, "Shipping Status Updated")
			return redirect('home')

		return render(request, "payment/not_shipped_dash.html", {
            'page_title': 'Un-shipped Dashboard',
            'orders':orders
        })
	else:
		messages.success(request, "Access Denied")
		return redirect('home')


def shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=True)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# grab the order
			order = Order.objects.filter(id=num)
			# grab Date and time
			now = datetime.datetime.now()
			# update order
			order.update(shipped=False)
			# redirect
			messages.success(request, "Shipping Status Updated")
			return redirect('home')

        
		return render(request, "payment/shipped_dash.html", {
            'page_title': 'Shipped Dashboard',
            'orders':orders
        })
	else:
		messages.success(request, "Access Denied")
		return redirect('home')


def process_order(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        
        
        # get billing info from last page
        payment_form = PaymentForm(request.POST or None)
        # get shipping session data
        my_shipping = request.session.get('my_shipping')

        # create shipping address from session info
        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
		# Create Shipping Address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_zipcode']}"
        amount_paid = totals
        
        if request.user.is_authenticated:
            # log in
            user = request.user
            # Create Order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

			# Add order items
			# Get the order ID
            order_id = create_order.pk
            
            # Get product Info
            for product in cart_products():
				# Get product ID
                product_id = product.id
				# Get product price
                price = product.price
                
                # Get quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
						# Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()
                        
            # delete cart after that
            for key in list(request.session.keys()):
                if key == "session_key":
					# Delete the key    
                    del request.session[key]
            
            messages.success(request, 'Order Placed')
            return redirect('store:home')
        else:
            messages.success(request, 'You must be logged in...')
            return redirect('store:home')
        
    else:
        messages.success(request, 'Access Denied')
        return redirect('store:home')

def billing_info(request):
    if request.POST:
        # get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        
        # create a session with shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        
        # check user 
        if request.user.is_authenticated:
            # get the billing form
            billing_form = PaymentForm()
            context = {
                'page_title': 'Billing Info',
                'cart_products': cart_products,
                'quantities': quantities,
                'totals': totals,
                'shipping_info': request.POST,
                'billing_form': billing_form,
            }
            return render(request, 'payment/billing_info.html', context)
        else:
            messages.success(request, 'You Must be Logged in...')
            return redirect('store:login') 
        
    else:
        messages.success(request, 'Access Denied')
        return redirect('store:home')
    

def checkout(request):
    # get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    if request.user.is_authenticated:
        # Checkout as logged in user
		# Shipping User
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        context = {
            'page_title': 'Checkout',
            'cart_products': cart_products,
            'quantities': quantities,
            'totals': totals,
            'shipping_form': shipping_form,
        }
        return render(request, 'payment/checkout.html', context)
    else:
        messages.success(request, 'You Must be Logged in...')
        return redirect('store:login')   

def payment_success(request):
    context = {'page_title': 'Payment Success'}
    return render(request, 'payment/payment_success.html', context)