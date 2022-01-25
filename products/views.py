from django.shortcuts import render
from products.models import Product, ProductCategory
from django.views.generic.list import ListView

from baskets.models import Basket


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
            context['basket_content'] = [basket.product.id for basket in self.request.user.basket_set.prefetch_related('product')]
        context['categories'] = ProductCategory.objects.all()
        context['title'] = 'GeekShop - Каталог'
        return context
