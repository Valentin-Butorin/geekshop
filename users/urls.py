from django.urls import path
from users.views import LogoutRedirectView, LoginFormView, RegistrationFormView, ProfileFormView, VerifyView

app_name = 'users'

urlpatterns = [
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutRedirectView.as_view(), name='logout'),
    path('registration/', RegistrationFormView.as_view(), name='registration'),
    path('profile/', ProfileFormView.as_view(), name='profile'),
    path('verify/<str:email>/<str:activation_key>/', VerifyView.as_view(), name='verify'),
]
