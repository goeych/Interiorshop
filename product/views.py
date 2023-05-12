from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Q
from django.contrib import messages
import random

from cart.cart import Cart

from .models import Product,Category
from .forms import AddToCartForm

# Create your views here.

def product(request,category_slug,product_slug):
    cart = Cart(request)
    product = get_object_or_404(Product,category__slug=category_slug,slug=product_slug)

    if request.method =='POST':
        form = AddToCartForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            cart.add(product_id = product.id,quantity=quantity, update_quantity = False)

            messages.success(request,'The product was added to the cart.')

            return redirect('product',category_slug= category_slug,product_slug=product_slug)
    else:
        form = AddToCartForm()

    similar_products = list(product.category.products.exclude(id=product.id))
    if len(similar_products) >= 4:
        similar_products = random.sample(similar_products,4)
    
    context={'product':product,'similar-products':similar_products,
             'form':form}
    return render(request,'product/product.html',context)

def category(request,category_slug):
    category = get_object_or_404(Category,slug = category_slug)
    
    context = {'category':category}
    return render(request,'product/category.html',context)

def search(request):
    query = request.GET.get('query','')
    products = Product.objects.filter(Q(title__icontains=query)|Q(description__icontains=query))

    context = {'products':products,'query':query}
    return render(request,'product/search.html',context)

