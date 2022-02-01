from django.shortcuts import render
from products.models import Product, ProductCategory
from django.views.generic.list import ListView

from django.core.cache import cache
from django.conf import settings
from django.views.decorators.cache import cache_page


def get_categories():
    if settings.LOW_CACHE:
        key = 'categories'
        categories = cache.get(key)
        if categories is None:
            categories = ProductCategory.objects.all()
            cache.set(key, categories)
        return categories
    else:
        return ProductCategory.objects.all()


# @cache_page(3600)
def index(request):
    context = {'title': 'Geekshop'}
    return render(request, 'products/index.html', context)


class ProductsListView(ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        category_id = self.kwargs.get('pk')
        if object_list:
            queryset = object_list
        else:
            if category_id:
                queryset = self.object_list.filter(category_id=category_id)
            else:
                queryset = self.object_list

        page_size = self.get_paginate_by(queryset)
        context_object_name = self.get_context_object_name(queryset)
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
            context = {
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'object_list': queryset
            }
        else:
            context = {
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'object_list': queryset
            }
        if context_object_name is not None:
            context[context_object_name] = queryset
        context.update(kwargs)

        if self.request.user.is_authenticated:
            baskets = self.request.user.basket_set.select_related('product')
            if baskets:
                context['basket_content'] = [basket.product.id for basket in baskets]
                baskets_total_sum = baskets[0].get_total_sum
                context['basket_total_sum'] = 0.0
                if baskets_total_sum:
                    context['basket_total_sum'] = baskets_total_sum

        context['categories'] = get_categories()
        context['title'] = 'GeekShop - Каталог'
        return context
