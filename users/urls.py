from django.urls import path
from users.views import registration, profile, LogoutRedirectView, LoginFormView

app_name = 'users'

urlpatterns = [
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutRedirectView.as_view(), name='logout'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
]
