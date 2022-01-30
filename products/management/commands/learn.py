from django.core.management.base import BaseCommand
from django.db.models import Q

from products.models import Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        products_list = Product.objects.filter(Q(category__name='Одежда') | Q(category__name='Обувь'))

        print(products_list)
