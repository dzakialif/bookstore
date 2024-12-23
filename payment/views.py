import datetime
from django.contrib import messages
from django.shortcuts import redirect, render
from cart.cart import Cart
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ShippingForm, PaymentForm
from .models import ShippingAddress, Order, OrderItem, PaymentInfo
from store.models import Profile
import datetime

# Create your views here.

def is_staff_admin(user):
    """
    Check if the user is in the staff_admin group or is a superuser.
    """
    return user.groups.filter(name='staff_admin').exists()

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'payment/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        # Filter orders by the logged-in user
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add related items and payment info to the context
        context['page_title'] = 'Order Detail'
        context['items'] = self.object.orderitem_set.all()
        context['payment'] = getattr(self.object, 'payment', None)  # Access related payment info
        return context

    def handle_no_permission(self):
        # Redirect unauthorized users
        messages.error(self.request, "You must be logged in to view your order details.")
        return redirect('store:login')

class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'payment/order_history.html'
    context_object_name = 'orders'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Order History'
        return context
    

    def get_queryset(self):
        # Filter orders by the logged-in user
        return super().get_queryset().filter(user=self.request.user).order_by('-date_ordered')

    def handle_no_permission(self):
        # Redirect unauthorized users
        messages.error(self.request, "You must be logged in to view your order history.")
        return redirect('store:login')


def payment_detail(request, pk):
    if request.user.is_authenticated:
        # Ambil payment info berdasarkan ID
        payment = PaymentInfo.objects.get(id=pk)

        # Periksa apakah user memiliki akses ke payment ini
        if payment.user != request.user and not (is_staff_admin(request.user) or request.user.is_superuser):
            messages.error(request, "You do not have permission to view this payment.")
            return redirect('store:home')

        # Handle POST request to update status
        if request.method == 'POST':
            new_status = request.POST.get('status')
            if new_status in dict(PaymentInfo.STATUS_CHOICES):  # Validasi pilihan status
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

def payment_dashboard(request):
    if request.user.is_authenticated and (is_staff_admin(request.user) or request.user.is_superuser):
        # Ambil semua payment info dari database
        payments = PaymentInfo.objects.all().order_by('-created_at')

        # Render halaman dashboard
        context = {
            'page_title': 'Payment Dashboard',
            'payments': payments,
        }
        return render(request, 'payment/payment_dashboard.html', context)
    else:
        messages.error(request, "Access Denied. You do not have permission to view this page.")
        return redirect('store:home')


def orders(request, pk):
	if request.user.is_authenticated and (is_staff_admin(request.user) or request.user.is_superuser):
		# Get the order
		order = Order.objects.get(id=pk)
		# Get the order items
		items = OrderItem.objects.filter(order=pk)

		if request.POST:
			status = request.POST['shipping_status']
			# Check if true or false
			if status == "true":
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				now = datetime.datetime.now()
				order.update(shipped=True, date_shipped=now)
			else:
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				order.update(shipped=False)
			messages.success(request, "Shipping Status Updated")
			return redirect('store:home')


		return render(request, 'payment/orders.html', {"order":order, "items":items})

	else:
		messages.success(request, "Access Denied")
		return redirect('store:home')


def not_shipped_dash(request):
	if request.user.is_authenticated and (is_staff_admin(request.user) or request.user.is_superuser):
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
			return redirect('store:home')

		return render(request, "payment/not_shipped_dash.html", {
            'page_title': 'Un-shipped Dashboard',
            'orders':orders
        })
	else:
		messages.success(request, "Access Denied")
		return redirect('store:home')


def shipped_dash(request):
	if request.user.is_authenticated and (is_staff_admin(request.user) or request.user.is_superuser):
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
			return redirect('store:home')

        
		return render(request, "payment/shipped_dash.html", {
            'page_title': 'Shipped Dashboard',
            'orders':orders
        })
	else:
		messages.success(request, "Access Denied")
		return redirect('store:home')


def process_order(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Get billing info from last page
        payment_form = PaymentForm(request.POST or None)
        # Get shipping session data
        my_shipping = request.session.get('my_shipping')

        # Create shipping address from session info
        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        shipping_address = f"{my_shipping['shipping_address']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_zipcode']}"
        amount_paid = totals

        if request.user.is_authenticated:
            # Log in
            user = request.user

            # Validate payment form
            if not payment_form.is_valid():
                messages.error(request, 'Invalid payment details. Please check the form and try again.')
                context = {
                    'page_title': 'Billing Info',
                    'cart_products': cart.get_prods(),
                    'quantities': cart.get_quants(),
                    'totals': cart.cart_total(),
                    'billing_form': payment_form,  # Return form with errors
                    'shipping_info': my_shipping,
                }
                return render(request, 'payment/billing_info.html', context)  # Render page with form

            # Create Order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Save payment info
            payment_info = PaymentInfo.objects.create(
                user=user,
                order=create_order,
                card_name=payment_form.cleaned_data['card_name'],
                card_number=payment_form.cleaned_data['card_number'],
                card_cvv=payment_form.cleaned_data['card_cvv_number'],
                status='pending',  # Initial status
            )
            # Add order items
            for product in cart_products():
                product_id = product.id
                price = product.price

                for key, value in quantities().items():
                    if int(key) == product.id:
                        OrderItem.objects.create(order=create_order, product_id=product_id, user=user, quantity=value, price=price)

            # Update payment status
            payment_info.save()

            # Delete cart after that
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            # Delete Cart from Database (old_cart field)
            current_user = Profile.objects.filter(user__id=request.user.id)
            current_user.update(old_cart="")

            messages.success(request, 'Order and payment processed successfully!')
            return redirect('store:home')
        else:
            messages.error(request, 'You must be logged in...')
            return redirect('store:home')

    else:
        messages.error(request, 'Access Denied')
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
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user, require_all_fields=True)
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