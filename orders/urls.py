from django.urls import path
from . import views
app_name = 'Orders'

urlpatterns = [
    path('', views.order_history, name='orders_home'),
    path('order-history/', views.order_history, name='order_history'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order_detail'),
]
