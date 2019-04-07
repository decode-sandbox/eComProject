from e_shop.models import Product, User
from django.contrib.auth.models import User as AuthUser
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

# Here are our views.

def home(request):
    p = Product.objects.all()[:4] #take four first products
    return render(request, 'e_shop/home.html', {'products':p})

@login_required(login_url='/eshop/login')
def shop(request,page_number=1):
    products_paginator = None 
    if 'products_paginator' in request.session:
        products_paginator = request.session['products_paginator']
    else:
        products = Product.objects.all()
        products_paginator = Paginator(products,4)
    current_products = list()
    try:
        current_products = products_paginator.page(page_number)
    except:
        current_products = products_paginator.page(0)
    return render(request, 'e_shop/shop.html', {'products': current_products})


def product(request):
    return render(request, 'e_shop/product.html')

def cart(request):
    return render(request, 'e_shop/cart.html')

def contact(request):
    return render(request, 'e_shop/contact.html')

def about(request):
    return render(request, 'e_shop/about.html')

def register(request):
    if request.method == "POST":
        form_values = request.POST.dict()
        username = form_values["username"]
        email = form_values["email"]
        password = form_values["password"]
        password_confirmation = form_values["confirm_password"]
        error = "Password and his confirmation are different"
        if password==password_confirmation:
            try:
                user = AuthUser.objects.create_user(username,email,password)
            except IntegrityError:
                error = f"Username {username} is already taken"
            else:
                User(user=user).save()
                login(request, user)
                return redirect(shop)
        return render(request, 'e_shop/register.html', {"error": error})    
    else:
        return render(request, 'e_shop/register.html')
    
def log_in(request):
    if request.method == "POST":
        form_values = request.POST.dict()
        username = form_values["username"]
        password = form_values["password"]
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(shop)
        else:
            return render(request,'e_shop/login.html', {"we_have_error": True})
    else:
        return render(request, 'e_shop/login.html')
    
def log_out(request):
    logout(request)
    return redirect(log_in)
