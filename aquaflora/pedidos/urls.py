from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('', views.pagina_pedidos_auth, name='pagina_pedidos'),
    path('cancel/<slug:id>', views.cancelar_pedido,name='cancelar_pedido'),
    path('pagar/<slug:id>', views.pagar_pedido, name='pagar_pedido'),
]