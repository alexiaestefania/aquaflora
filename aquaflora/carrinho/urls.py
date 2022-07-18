from django.urls import path
from . import views

app_name = 'carrinho'

urlpatterns = [
    path('', views.carrinhoresumo, name='carrinhoresumo'),
    path('add/', views.carrinho_add, name='carrinho_add'),
    ]