from django.shortcuts import render
from e_shop.models import Product

# Here are our views.

def home(request):
    p = Product.objects.all()[:4] #take four first products
    return render(request,'e_shop/home.html',{'products':p})

def shop(request):
    return render(request,'e_shop/shop.html')

def product(request):
    pr = Product.objects.all()
    paginator = Paginator(pr, 25)

    page = request.GET.get('page')
    products = paginator.get_page(page)
    return render(request, 'e_shop/product.html', {'products': products})

def cart(request):
    return render(request,'e_shop/cart.html')

def contact(request):
    return render(request,'e_shop/contact.html')


def about(request):
    return render(request, 'e_shop/about.html')


