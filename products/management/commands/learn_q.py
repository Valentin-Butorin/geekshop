from django.core.management.base import BaseCommand
from django.db.models import Q

from products.models import Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        min_price = 5000
        max_price = 20000

        products_by_price_range = Product.objects.filter(
            (Q(category__name='Одежда') | Q(category__name='Обувь')) &
            (Q(price__gte=min_price) & Q(price__lte=max_price))
        ).select_related()

        print(products_by_price_range)
