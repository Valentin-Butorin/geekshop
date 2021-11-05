from django.contrib import auth, messages
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView, FormView

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from baskets.models import Basket


class LoginFormView(FormView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('index')
    form_class = UserLoginForm

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return super(LoginFormView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return super(LoginFormView, self).get(request, *args, **kwargs)


class LogoutRedirectView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return super(LogoutRedirectView, self).get(request, *args, **kwargs)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'title': 'GeekShop - Регистрация', 'form': form}
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))

    form = UserProfileForm(instance=request.user)
    context = {
        'title': 'GeekShop - Профиль',
        'form': form,
        'baskets': Basket.objects.filter(user_id=request.user),
    }
    return render(request, 'users/profile.html', context)
