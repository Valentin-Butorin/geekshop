from django.shortcuts import render
from products.models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
        context = super(ProductsListView, self).get_context_data(object_list=None, **kwargs)
        category_id = self.kwargs.get('pk')
        if category_id:
            context['object_list'] = self.model.objects.filter(category_id=category_id)
            print(context)
        context['categories'] = ProductCategory.objects.all()
        return context
