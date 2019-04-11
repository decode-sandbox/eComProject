from e_shop.models import Product, User, Purchase
from django.contrib.auth.models import User as AuthUser
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

# Here are our views.
def root(request):
    return redirect(home)

def home(request):
    p = Product.objects.all()[:4] #take four first products
    return render(request, 'e_shop/home.html', {'products':p})

@login_required(login_url='/eshop/login')
def shop(request,page_number=1):
    if request.method == "POST": #if the cart is updated
        form_values = request.POST.dict()
        product_id = form_values["id"]
        n = form_values["number_to_purchase"]
        request.session['cart'][product_id] = int(n)
        
    number_of_products_per_page = 4
    products_paginator = None
    products = Product.objects.all()
    products_paginator = Paginator(products,number_of_products_per_page)
    if 'cart' not in request.session:
        request.session['cart'] = dict()
        for product in products:
            request.session['cart'][str(product.id)] = 0     
    current_products = list()
    try:
        current_products = products_paginator.page(page_number)
    except:
        current_products = products_paginator.page(0)
    return render(request, 'e_shop/shop.html', {'products': current_products,
                                                'cart': request.session['cart']})
    
def product(request):
    return render(request, 'e_shop/product.html')

def cart(request):
    if request.method == "POST":
        form_values = request.POST.dict()
        for key,value in form_values.items():
            if key != 'csrfmiddlewaretoken':
                product_id,number = key,int(value)
                p = Product.objects.get(id=product_id)
                p.quantity -= number
                p.save()
                c = User.objects.get(user=request.user)
                Purchase.objects.create(quantity=number, product=p, client=c)
        try:
            del request.session['cart']
        except KeyError:
            pass
        return render(request, 'e_shop/bought.html')
    user_cart = dict()
    amount = 0
    for product_id,number in request.session['cart'].items():
        product = Product.objects.get(id=product_id)
        if number!=0:
            user_cart[product.name] = {"number": number, "id": product_id,
                     "max_number": product.quantity, "price": product.price}
            amount += number*product.price
    return render(request, 'e_shop/cart.html', {'cart': user_cart,
                                                'amount' : amount})

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
    return redirect(home)
