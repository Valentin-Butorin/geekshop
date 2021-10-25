from django.shortcuts import HttpResponseRedirect
from products.models import Product
from baskets.models import Basket
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        if basket.quantity < product.quantity:
            basket.quantity += 1
            basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


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
