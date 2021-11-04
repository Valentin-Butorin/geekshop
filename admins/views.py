from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from users.models import User
from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm, CategoryAdminFrom
from products.models import ProductCategory


@user_passes_test(lambda u: u.is_staff)
def index(request):
    context = {
        'title': 'GeekShop - Админ Панель'
    }
    return render(request, 'admins/index.html', context)


class UserListView(ListView):
    model = User
    template_name = 'admins/admin-users-read.html'


class UserCreateView(CreateView):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegistrationForm
    success_url = reverse_lazy('admins:admin_users')


class UserUpdateView(UpdateView):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')


class UserDeleteView(DeleteView):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    success_url = reverse_lazy('admins:admin_users')


@user_passes_test(lambda u: u.is_staff)
def admin_categories(request):
    context = {
        'title': 'GeekShop - Категории',
        'categories': ProductCategory.objects.all()
    }
    return render(request, 'admins/admin-categories-read.html', context)


@user_passes_test(lambda u: u.is_staff)
def admin_categories_create(request):
    if request.method == 'POST':
        form = CategoryAdminFrom(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_categories'))

    form = CategoryAdminFrom()
    context = {
        'title': 'GeekShop - Создание категории',
        'form': form,
    }
    return render(request, 'admins/admin-categories-create.html', context)


@user_passes_test(lambda u: u.is_staff)
def admin_categories_update(request, id):
    selected_category = ProductCategory.objects.get(id=id)
    if request.method == 'POST':
        form = CategoryAdminFrom(data=request.POST, instance=selected_category)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_categories'))

    form = CategoryAdminFrom(instance=selected_category)
    context = {
        'title': 'GeekShop - Редактирование категории',
        'form': form,
        'selected_category': selected_category,
    }
    return render(request, 'admins/admin-categories-update-delete.html', context)


@user_passes_test(lambda u: u.is_staff)
def admin_categories_delete(request, id):
    category = ProductCategory.objects.get(id=id)
    category.delete()
    return HttpResponseRedirect(reverse('admins:admin_categories'))
