from django.shortcuts import render

from product.models import Product

# Create your views here.

def frontpage(request):

    newest_products = Product.objects.all()[0:8]

    context = {'newest_products':newest_products}
    return render(request,'core/frontpage.html',context)

def contact(request):

    context = {}
    return render(request,'core/contact.html',context)
