from django.urls import path
from users.views import profile, LogoutRedirectView, LoginFormView, RegistrationFormView

app_name = 'users'

urlpatterns = [
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutRedirectView.as_view(), name='logout'),
    path('registration/', RegistrationFormView.as_view(), name='registration'),
    path('profile/', profile, name='profile'),
]
