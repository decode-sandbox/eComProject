from django.shortcuts import render
from e_shop.models import Product
from django.core.paginator import Paginator

# Here are our views.

def home(request):
    p = Product.objects.all()[:4] #take four first products
    return render(request,'e_shop/home.html',{'products':p})

def shop(request):
    pro = Product.objects.all()
    paginator = Paginator(pro, 2)  # Show 2 contacts per page
    page = request.GET.get('page')
    context = {'products': pro}
    template = 'e_shop/shop.html'
    products = paginator.get_page(page)
    return render(request,template,context)


def product(request):
    return render(request,'e_shop/product.html')

def cart(request):
    return render(request,'e_shop/cart.html')

def contact(request):
    return render(request,'e_shop/contact.html')

def about(request):
    return render(request, 'e_shop/about.html')


