from django.urls import path
from users.views import login, registration, profile, LogoutRedirectView

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', LogoutRedirectView.as_view(), name='logout'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
]
