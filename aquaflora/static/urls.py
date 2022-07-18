from django.urls import path
from . import views

app_name = 'conta'

urlpatterns = [
    path('registrar/', views.criar_conta, name='registrar'),
    path('ativar/<slug:uidb64>/<slug:token>/', views.ativar_conta, name='ativar'),
    path('perfil/', views.perfil, name='perfil'),
    path('login/', views.login, name='login'),
    ]