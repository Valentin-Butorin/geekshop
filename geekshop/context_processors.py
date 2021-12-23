from baskets.models import Basket


def baskets(request):
    basket_items = []

    if request.user.is_authenticated:
        basket_items = Basket.objects.filter(user_id=request.user)

    return {'baskets': basket_items}
