from django.db import models
from users.models import User
from products.models import Product


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity

    def total_sum(self):
        baskets = Basket.objects.filter(user_id=self.user)
        sum_total = sum(basket.sum() for basket in baskets)
        return sum_total

    def total_quantity(self):
        return Basket.objects.filter(user_id=self.user).aggregate(models.Sum('quantity'))['quantity__sum']
