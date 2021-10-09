from django.shortcuts import render
from json import load, decoder
from datetime import datetime


# Create your views here.
def index(request):
    current_date = datetime.now()
    context = {
        'title': 'Geekshop',
        'current_date': current_date
    }
    return render(request, 'products/index.html', context)


def products(request):
    products_list = parse_json('products/fixtures/products.json')
    context = {
        'title': 'Geekshop - Каталог',
        'products': products_list,
        'card_template': 'products/card_template.html'
    }
    return render(request, 'products/products.html', context)


def parse_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return load(f)
    except FileNotFoundError:
        return []
    except decoder.JSONDecodeError:
        return []
