from django.shortcuts import render
from products.models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from baskets.models import Basket


def index(request):
    context = {'title': 'Geekshop'}
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page=1):
    basket_content = []
    if request.user.is_authenticated:
        basket_content = [basket.product.id for basket in Basket.objects.filter(user=request.user)]

    context = {
        'title': 'Geekshop - Каталог',
        'categories': ProductCategory.objects.all(),
        'basket_content': basket_content,
    }

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    paginator = Paginator(products, 3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context['products'] = products_paginator
    return render(request, 'products/products.html', context)
