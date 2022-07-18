from django.urls import path
from . import views

app_name = 'aquaflora_stats'

urlpatterns = [
    path('populares', views.BestSeller, name='BestSeller'), 
    path('estoque', views.Estoquereport, name='Estoquereport'), 
    path('financeiro', views.FinanceiroReport, name='FinanceiroReport'), 
    ]