from django.core.management.base import BaseCommand
from django.db.models import Q, F, When, Case, DecimalField, IntegerField

from orders.models import OrderItem
from products.models import Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Скидка при заказе товара с ценой от 2000 до 4999 - 5%
        Скидка при заказе товара с ценой от 5000 до 9999 - 10%
        Скидка при заказе товара с ценой от 10000 - 15%
        """

        action_1 = 1
        action_2 = 2
        action_3 = 3

        action_1_range = (2000, 4999)
        action_2_range = (5000, 9999)
        action_3_range = (10000,)

        action_1_discount = 0.05
        action_2_discount = 0.1
        action_3_discount = 0.15

        action_1_condition = Q(product__price__gte=action_1_range[0]) & \
                             Q(product__price__lte=action_1_range[1])

        action_2_condition = Q(product__price__gte=action_2_range[0]) & \
                             Q(product__price__lte=action_2_range[1])

        action_3_condition = Q(product__price__gte=action_3_range[0])

        action_1_order = When(action_1_condition, then=action_1)
        action_2_order = When(action_2_condition, then=action_2)
        action_3_order = When(action_3_condition, then=action_3)

        action_1_value = When(action_1_condition, then=F('product__price') * F('quantity') * action_1_discount)
        action_2_value = When(action_2_condition, then=F('product__price') * F('quantity') * action_2_discount)
        action_3_value = When(action_3_condition, then=F('product__price') * F('quantity') * action_3_discount)

        orderitems = OrderItem.objects.annotate(
            action_order=Case(
                action_1_order,
                action_2_order,
                action_3_order,
                output_field=DecimalField()
            )
        ).annotate(
            discount_value=Case(
                action_1_value,
                action_2_value,
                action_3_value,
                output_field=DecimalField()
            )
        ).order_by('action_order', 'discount_value').select_related()

        for item in orderitems:
            print(f'Action: {item.action_order:1} order: #{item.order.pk:3} product: {item.product.name:50} '
                  f'price: {item.product.price:10} discount value: {item.discount_value:10.2f} '
                  f'discount price: {item.product.price - item.discount_value:10}')
