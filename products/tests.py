from django.test import TestCase
from products.models import ProductCategory, Product


class TestProductsSmoke(TestCase):
    success_status_code = 200

    def setUp(self) -> None:
        for i in range(10):
            cat = ProductCategory.objects.create(name=f'cat{i}')
            Product.objects.create(
                name=f'product{i}',
                price=i,
                quantity=i,
                category=cat,
                image='test'
            )

    def test_categories_urls(self):
        for cat in ProductCategory.objects.all():
            response = self.client.get(f'/products/{cat.pk}/')
            self.assertEqual(response.status_code, self.success_status_code)
