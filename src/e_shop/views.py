from django.shortcuts import render

# Here are our views.

def home(request):
    return render(request,'e_shop/home.html')

def shop(request):
    return render(request,'e_shop/shop.html')

def product(request):
    return render(request,'e_shop/product.html')

def cart(request):
    return render(request,'e_shop/cart.html')