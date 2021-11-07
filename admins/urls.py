from django.urls import path
from admins.views import index, UserCreateView, UserListView, UserUpdateView, UserDeleteView, \
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='admin_users'),
    path('users_create/', UserCreateView.as_view(), name='admin_users_create'),
    path('users_update/<int:pk>/', UserUpdateView.as_view(), name='admin_users_update'),
    path('users_delete/<int:pk>/', UserDeleteView.as_view(), name='admin_users_delete'),
    path('categories/', CategoryListView.as_view(), name='admin_categories'),
    path('categories_create/', CategoryCreateView.as_view(), name='admin_categories_create'),
    path('categories_update/<int:pk>/', CategoryUpdateView.as_view(), name='admin_categories_update'),
    path('categories_delete/<int:pk>/', CategoryDeleteView.as_view(), name='admin_categories_delete'),
]
