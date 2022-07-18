from django.urls import path
from . import views
app_name = 'wishlist'

urlpatterns = [
    path('', views.wishlist, name='wishlist'),
    path('add', views.wishlist_add, name='wishlist_add'),
    ]