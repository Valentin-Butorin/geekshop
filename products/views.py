from django.shortcuts import render
from products.models import Product, ProductCategory
from django.template.loader import render_to_string
from django.http import JsonResponse

from baskets.models import Basket


def index(request):
    context = {'title': 'Geekshop'}
    return render(request, 'products/index.html', context)


def products(request, category_id=None):
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
    context['products'] = products
    return render(request, 'products/products.html', context)
