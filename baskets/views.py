from products.models import Product, ProductCategory
from baskets.models import Basket
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.conf import settings


def basket_add(request, product_id):
    if request.is_ajax():
        response_dict = {
            'authenticated': request.user.is_authenticated,
            'result': ''
        }
        if not response_dict['authenticated']:
            response_dict['redirect_url'] = settings.LOGIN_URL
            return JsonResponse(response_dict)

        baskets = Basket.objects.filter(user=request.user)
        product = Product.objects.get(id=product_id)
        product_in_basket = baskets.filter(product=product)
        if not product_in_basket.exists():
            Basket.objects.create(user=request.user, product=product, quantity=1)
        else:
            basket = product_in_basket.first()
            basket.quantity += 1
            basket.save()

        context = {
            'products': Product.objects.all(),
            'categories': ProductCategory.objects.all(),
            'basket_content': [basket.product.id for basket in baskets],
        }
        response_dict['result'] = render_to_string('products/products_content.html', context)
        return JsonResponse(response_dict)


def basket_remove(request, id):
    if request.is_ajax():
        basket = Basket.objects.get(id=id)
        basket.delete()

        baskets = Basket.objects.filter(user=request.user)
        context = {'baskets': baskets}
        result = render_to_string('baskets/baskets.html', context)
        return JsonResponse({'result': result})


def basket_edit(request, id, quantity):
    if request.is_ajax():
        basket = Basket.objects.get(id=id)
        product_remains = basket.product.quantity
        if quantity > 0:
            if quantity <= product_remains:
                basket.quantity = quantity
                basket.save()
        else:
            basket.delete()

        baskets = Basket.objects.filter(user=request.user)
        context = {'baskets': baskets}
        result = render_to_string('baskets/baskets.html', context)
        return JsonResponse({'result': result})
