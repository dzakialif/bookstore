from django.urls import path
from . import views
from .views import HomeView, AboutView, ProductDetailView

app_name = 'store'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_info/', views.update_info, name='update_info'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product'),
    path('category/<slug>', views.category, name='category'),
]