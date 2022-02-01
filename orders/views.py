from django.db import transaction
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import HttpResponseRedirect
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView

from baskets.models import Basket
from orders.forms import OrderItemForm
from orders.models import Order, OrderItem
from products.models import Product


class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class OrderCreateView(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.method == 'POST':
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items.exists():
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=basket_items.count())
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
            else:
                formset = OrderFormSet()

        context_data['orderitems'] = formset

        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        orderitems = context_data['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        basket_items = Basket.objects.filter(user=self.request.user)
        basket_items.delete()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderUpdateView(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.method == 'POST':
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

        context_data['orderitems'] = formset

        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        orderitems = context_data['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderDetailView(DetailView):
    model = Order


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('orders:list')


def complete(request, pk):
    order_item = Order.objects.get(pk=pk)
    order_item.status = Order.STATUS_SEND_TO_PROCEED
    order_item.save()
    return HttpResponseRedirect(reverse('orders:list'))


def get_price(request, pk):
    if request.is_ajax():
        response = {'price': None}

        product = Product.objects.get(pk=pk)

        if product:
            response['price'] = product.price

        return JsonResponse(response)
