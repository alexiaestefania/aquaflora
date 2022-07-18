from django.urls import path
from . import views
app_name = 'user_manual'

urlpatterns = [
    path('', views.user_manual, name='user_manual'),
    ]