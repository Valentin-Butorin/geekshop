from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView

from users.models import User
from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm, CategoryAdminFrom
from products.models import ProductCategory


@user_passes_test(lambda u: u.is_staff)
def index(request):
    context = {
        'title': 'GeekShop - Админ Панель'
    }
    return render(request, 'admins/index.html', context)


@user_passes_test(lambda u: u.is_staff)
def admin_users_create(request):
    if request.method == 'POST':
        form = UserAdminRegistrationForm(files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_users'))
    else:
        form = UserAdminRegistrationForm()

    context = {
        'title': 'GeekShop - Создание пользователя',
        'form': form
    }
    return render(request, 'admins/admin-users-create.html', context)


class UserListView(ListView):
    model = User
    template_name = 'admins/admin-users-read.html'


@user_passes_test(lambda u: u.is_staff)
def admin_users_update(request, id):
    selected_user = User.objects.get(id=id)
    if request.method == 'POST':
        form = UserAdminProfileForm(instance=selected_user, files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_users'))

    form = UserAdminProfileForm(instance=selected_user)
    context = {
        'title': 'GeekShop - Обновление пользователя',
        'form': form,
        'selected_user': selected_user,
    }
    return render(request, 'admins/admin-users-update-delete.html', context)


@user_passes_test(lambda u: u.is_staff)
def admin_users_delete(request, id):
    user = User.objects.get(id=id)
    user.safe_delete()
    return HttpResponseRedirect(reverse('admins:admin_users'))


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
