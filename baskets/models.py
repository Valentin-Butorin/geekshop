from django.db import models
from users.models import User
from products.models import Product

from django.utils.functional import cached_property


class BasketQuerySet(models.QuerySet):
	def delete(self, *args, **kwargs):
		for item in self:
			item.product.quantity += item.quantity
			item.product.save()
		super().delete(*args, **kwargs)


class Basket(models.Model):
	objects = BasketQuerySet().as_manager()

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=0)
	created_timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'Корзина для {self.user.username} | Продукт {self.product.name}'

	def sum(self):
		return self.product.price * self.quantity

	def total_sum(self):
		return sum(basket.sum() for basket in self.baskets)

	def total_quantity(self):
		return sum(basket.quantity for basket in self.baskets)

	@cached_property
	def get_items_cached(self):
		return self.user.basket_set.select_related()

	@property
	def get_total_quantity(self):
		_items = self.get_items_cached
		return sum(item.quantity for item in _items)

	@property
	def get_total_sum(self):
		_items = self.get_items_cached
		return sum(item.quantity * item.product.price for item in _items)

	@property
	def baskets(self):
		return Basket.objects.filter(user_id=self.user).select_related()
