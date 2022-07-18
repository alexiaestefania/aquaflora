

from django.contrib import admin

from .models import ItemPedido, Pedido


class ItemInline(admin.TabularInline):
    model = ItemPedido
    raw_id_fields = ["produto"]
    extra = 0

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ["__str__", "criadoem", "valorpgto", "statuspgto", "Destinatario", "Endereco",  "userFrete", "statusentrega"]
    readonly_fields = ["__str__","criadoem", "valorpgto", "Destinatario", "Endereco",  "userFrete"]
    list_filter = ["criadoem", "statuspgto", 'statusentrega']
    inlines = [ItemInline]