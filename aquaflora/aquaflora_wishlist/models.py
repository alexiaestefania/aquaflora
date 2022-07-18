from django.db import models
from django.conf import settings
from aquaflorastore.models import Produto

# Create your models here.
class User_Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="usuario_wishlist",
        verbose_name="Usuário",
        blank=True,
        editable=False,
    )
    wishlist_item  = models.ForeignKey(
        Produto, 
        related_name="Item_Favoritado", 
        on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.user.username