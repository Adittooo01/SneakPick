from django.urls import path
from . import views

urlpatterns = [
    path('', views.shipping_Methods, name='shipping_home'),
    path('shipping-methods/', views.shipping_Methods, name='shipping_methods'),
]
