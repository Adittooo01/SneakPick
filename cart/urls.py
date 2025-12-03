from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.render_cart, name='render_cart'),
    path('cart/', views.render_cart, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
]