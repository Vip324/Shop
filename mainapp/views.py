from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import cache_page
import random
from mainapp.models import ProductCategory, Product


def get_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = 'category_{}'.format(pk)
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = 'product_{}'.format(pk)
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = 'products_in_category_orederd_by_price_{}'.format(pk)
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True). \
                order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True). \
            order_by('price')

# Переделанные под новые функции

def catalog(request, pk, page=1):
    # print('NOT AJAX')
    if pk == '0':
        category = {
            'pk': 0,
            'name': 'All'
        }
        products = get_products_orederd_by_price()
    else:
        category = get_category(pk)
        products = get_products_in_category_orederd_by_price(pk)
    paginator = Paginator(products, 2)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context = {
        'page_title': 'catalog',
        'category': category,
        'products': products_paginator,
        'catalog_menu': get_menu(),
    }
    return render(request, 'mainapp/products.html', context)

@cache_page(240)
def catalog_ajax(request, pk, page=1):
    if request.is_ajax():
        # print('AJAX')
        links_menu = get_menu()

        if pk:
            if pk == '0':
                category = {
                    'pk': 0,
                    'name': 'ALL'
                }
                products = get_products_orederd_by_price()
            else:
                category = get_category(pk)
                products = get_products_in_category_orederd_by_price(pk)

            paginator = Paginator(products, 2)
            try:
                products_paginator = paginator.page(page)
            except PageNotAnInteger:
                products_paginator = paginator.page(1)
            except EmptyPage:
                products_paginator = paginator.page(paginator.num_pages)

            content = {
                'catalog_menu': links_menu,
                'category': category,
                'products': products_paginator,
            }

            result = render_to_string('mainapp/include_block/inc_products_content.html', context=content,
                                      request=request)

            return JsonResponse({'result': result})

def product(request, pk):
    context = {
        'page_title': 'product',
        'product': get_product(pk),
        'catalog_menu': get_menu(),
    }
    return render(request, 'mainapp/product.html', context)


def index(request):
    products = get_products()[:4]
    context = {
        'page_title': 'main',
        'products': products,
    }
    return render(request, 'mainapp/index.html', context)


def get_hot_product():
    return random.choice(get_products())


def get_same_products(hot_product):
    return hot_product.category.product_set.exclude(pk=hot_product.pk)


def products(request):
    products = get_products()
    context = {
        'page_title': 'prod',
        'products': products,
        'catalog_menu': get_menu(),
    }
    return render(request, 'mainapp/products.html', context)


def product_details(request):
    products = get_products()
    hot_product = get_hot_product()
    context = {
        'page_title': 'prod',
        'products': products,
        'catalog_menu': get_menu(),
        'hot_product': hot_product,
        'same_products': get_same_products(hot_product),
    }
    return render(request, 'mainapp/product_details.html', context)


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
    }
    return render(request, 'mainapp/contact.html', context)
