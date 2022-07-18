from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView
from . import views
from .forms import UserLoginForm

app_name = 'conta'

urlpatterns = [
    path('registrar/', views.criar_conta, name='registrar'),
    path('ativar/<slug:uidb64>/<slug:token>/', views.ativar_conta, name='ativar'),
    path('login/', auth_views.LoginView.as_view(template_name='conta/login.html', form_class=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/conta/login/'), name='logout'),
    
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/pedidos', views.perfilpedidos, name='perfilpedidos'),
    path('perfil/enderecos/', views.enderecos, name='enderecos'),
    
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),  
    path('perfil/excluir/', views.excluir_perfil, name='excluir_perfil'),
    path('perfil/delete_confirm/', TemplateView.as_view(template_name="conta/delete_confirm.html"), name='delete_confirmation_question'),
    path('perfil/delete_confirmed/', TemplateView.as_view(template_name="conta/delete_confirmed.html"), name='delete_confirmation'),
    
    path('perfil/endereco/adicionar', views.enderecos_add, name='enderecos_add'),
    path('perfil/enderecos/editar/<slug:id>', views.enderecos_edit, name='enderecos_edit'),
    path('perfil/enderecos/excluir/<slug:id>', views.enderecos_del, name='enderecos_del'),
    path('perfil/enderecos/defaultset/<slug:id>', views.enderecos_default, name='enderecos_default'),
    
    path('dashboard/', views.loginredirect, name='loginredirect'),                
    ]