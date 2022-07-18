from django.urls import path
from . import views

app_name = 'aquaflorastore'

urlpatterns = [
    path('', views.allproducts, name='allproducts'), #root, pagina principal q mostra todos os produtos
    path('produto/<slug:livro_slug>/', views.product_detail, name='product_detail'),
    path('categoria/<slug:cat_slug>/', views.categoriaview, name='categoriaview'),
    path('lancamentos', views.lancamentos, name='lancamentos'),
    path('promocoes', views.promo, name='promo'),
    path('bestsellers', views.bestseller, name='bestseller'),
    path('search/', views.search, name ='search'),
    path('sample/', views.samplepage, name = 'samplepage'),
    
    
    ]