from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='list'),
    path('create/', views.OrderCreateView.as_view(), name='create'),
    path('update/<pk>/', views.OrderUpdateView.as_view(), name='update'),
    path('read/<pk>/', views.OrderDetailView.as_view(), name='read'),
    path('delete/<pk>/', views.OrderDeleteView.as_view(), name='delete'),
    path('complete/<pk>/', views.complete, name='complete'),
]
