from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from mainapp.models import ProductCategory, Product
from django.urls import reverse
import random

def index(request):
    products = Product.objects.all()[:4]
    
    context = {
        'page_title': 'main',
        'products': products,
        'basket': get_basket(request),
    }
    return render(request, 'mainapp/index.html', context)

def get_basket(request):
    if request.user.is_authenticated:
        return request.user.basket.all()
    else:
        return []
    
def get_hot_product():
    return random.choice(Product.objects.all())

def get_same_products(hot_product):
    return hot_product.category.product_set.exclude(pk=hot_product.pk)


def products(request):
    products = Product.objects.all()

    context = {
        'page_title': 'prod',
        'products': products,
        'catalog_menu': get_menu(),
        'basket': get_basket(request),
    }
    return render(request, 'mainapp/products.html', context)

def product_details(request):
    products = Product.objects.all()
    hot_product = get_hot_product()

    context = {
        'page_title': 'prod',
        'products': products,
        'catalog_menu': get_menu(),
        'basket': get_basket(request),
        'hot_product': hot_product,
        'same_products': get_same_products(hot_product),
    }
    return render(request, 'mainapp/product_details.html', context)

def get_menu():
    return ProductCategory.objects.filter(is_active=True)


def catalog(request, pk):
    if pk == '0':
        category = {
            'pk': 0,
            'name': 'All'
        }
        products = Product.objects.all()
    
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        products = category.product_set.all()
    
    context = {
        'page_title': 'catalog',
        'category': category,
        'products': products,
        'catalog_menu': get_menu(),
        'basket': get_basket(request),
    }
    return render(request, 'mainapp/products.html', context)

def product(request, pk):
    context = {
        'page_title': 'product',
        'product': get_object_or_404(Product, pk=pk),
        'catalog_menu': get_menu(),
        'basket': get_basket(request),
    }
    return render(request, 'mainapp/product.html', context)

       
def contact(request):
    locations = [
        {
            'city': 'Moscow',
            'phone': '+7-888-888-8888',
            'email': 'info@geekshop.ru',
            'address': 'In the central of City'
        },
        {
            'city': 'Sankt-Peterburg',
            'phone': '+7-555-888-8888',
            'email': 'spb@geekshop.ru',
            'address': 'In the central of Old City'
        },
        {
            'city': 'Vladivostok',
            'phone': '+7-333-888-8888',
            'email': 'fareast@geekshop.ru',
            'address': 'Near the Central RailStation'
        },
    ]
    context = {
        'page_title': 'contact',
        'locations': locations,
        'basket': get_basket(request),
    }
    return render(request, 'mainapp/contact.html', context)
