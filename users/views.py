from django.contrib import auth, messages
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView, FormView
from django.views.generic.edit import UpdateView

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from baskets.models import Basket
from users.models import User


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

    def get_context_data(self, **kwargs):
        context = super(LoginFormView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Авторизация'
        return context


class LogoutRedirectView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return super(LogoutRedirectView, self).get(request, *args, **kwargs)


class RegistrationFormView(FormView):
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    form_class = UserRegistrationForm

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Вы успешно зарегистрировались!')
        return super(RegistrationFormView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return super(RegistrationFormView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RegistrationFormView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Регистрация'
        return context


class ProfileFormView(UpdateView):
    model = User
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    form_class = UserProfileForm
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(ProfileFormView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Профиль'
        context['baskets'] = Basket.objects.filter(user_id=self.request.user)
        return context

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        self.kwargs[self.pk_url_kwarg] = self.request.user.id
        return super(ProfileFormView, self).dispatch(request, *args, **kwargs)


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
