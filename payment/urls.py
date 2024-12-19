from django.urls import path

from . import views
from .views import OrderHistoryView, OrderDetailView

app_name = 'payment'

urlpatterns = [
    path('order_detail/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
    path('order_history/', OrderHistoryView.as_view(), name='order_history'),
    path('payment_detail/<int:pk>', views.payment_detail, name='payment_detail'),
    path('payment_dashboard/', views.payment_dashboard, name='payment_dashboard'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('checkout/', views.checkout, name='checkout'),
    path('billing_info/', views.billing_info, name='billing_info'),
    path('process_order/', views.process_order, name='process_order'),
    path('shipped_dash/', views.shipped_dash, name='shipped_dash'),
    path('not_shipped_dash/', views.not_shipped_dash, name='not_shipped_dash'),
    path('orders/<int:pk>', views.orders, name='orders'),
]