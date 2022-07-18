from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar

urlpatterns = [
    path('admin/reports/', include('aquaflora_stats.urls', namespace='aquaflora_stats')),
    path('admin/user_manual/', include('aquaflora_usermanual.urls', namespace='user_manual')),
    path('admin/', admin.site.urls),
    path('', include('aquaflorastore.urls', namespace='aquaflorastore')),
    path('carrinho/', include('carrinho.urls', namespace='carrinho')),
    path('conta/', include('conta.urls', namespace='conta')),
    path('wishlist', include('aquaflora_wishlist.urls',namespace='wishlist')),
    path('pedidos/', include('pedidos.urls', namespace='pedidos')),
    path('checkout/', include('aquaflora_checkout.urls', namespace='checkout')),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url("favicon.ico"))),
    path('__debug__/', include('debug_toolbar.urls')),
    
]

urlpatterns += static(
    settings.MEDIA_URL, document_root = settings.MEDIA_ROOT
    )