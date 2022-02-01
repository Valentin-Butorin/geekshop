from django.contrib import auth, messages
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView, FormView, TemplateView
from django.views.generic.edit import UpdateView

from baskets.models import Basket
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, UserAdditionalProfileForm
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

        messages.success(
            self.request,
            'Вы успешно зарегистрировались!'
            'Для подтверждения учетной записи перейдите по ссылке, '
            'отправленной на почтовый адрес, указанный Вами при регистрации')
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
        context['additional_profile_form'] = UserAdditionalProfileForm(instance=self.request.user.userprofile)
        baskets = self.request.user.basket_set.all().select_related('product').order_by('product__name')
        context['baskets'] = baskets
        context['total_quantity'] = sum(basket.quantity for basket in baskets)
        context['total_sum'] = sum(basket.quantity * basket.product.price for basket in baskets)
        return context

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        self.kwargs[self.pk_url_kwarg] = self.request.user.id
        return super(ProfileFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        profile_form = self.get_form(UserAdditionalProfileForm)
        profile_form.instance = self.request.user.userprofile

        if profile_form.is_valid():
            profile_form.save()
            return super().form_valid(form)

        return HttpResponseRedirect(reverse('users:profile'))


class VerifyView(TemplateView):
    template_name = 'users/verification.html'

    def get(self, request, *args, **kwargs):
        email = kwargs['email']
        activation_key = kwargs['activation_key']

        response = super().get(request, *args, **kwargs)
        response.context_data['user'] = None

        user = User.objects.filter(email=email).first()

        if user:
            if user.verify(email, activation_key):
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                response.context_data['user'] = user

        return response
