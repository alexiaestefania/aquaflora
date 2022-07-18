from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
   path('', views.paginacheckout, name='paginacheckout'), 
   path('updatefrete/', views.updatefrete, name='updatefrete'),
   path('pagamento', views.pagamento, name='pagamento'),
   path('status/', views.pagamento_status, name='status')
]