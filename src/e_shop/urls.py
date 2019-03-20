from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home),
    path('shop', views.shop),
    path('product',views.product),
    path('cart',views.cart),
    path('about', views.about),
    path('contact', views.contact)
]