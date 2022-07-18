from django.contrib import admin

from .models import Categoria, Produto, ProdutoEstoque


@admin.register(Categoria)
class CriaCat(admin.ModelAdmin):
    list_display = ["cat_nome", "cat_slug", "cat_ativa", "cat_criadoem", "created_by"]
    prepopulated_fields = {"cat_slug": ("cat_nome",)}


@admin.register(Produto)
class CriaProd(admin.ModelAdmin):
    list_display = [
        "livro_nome",
        "livro_autor",
        "livro_editora",
        "livro_qtdd",
        "livro_idioma",
        "livro_preco",
        "livro_estoque",
        "livro_ativo",
        "created_by",
        "livro_criadoem",
        "livro_atualizadoem",
    ]
    list_filter = ["livro_estoque", "livro_ativo"]
    list_editable = ["livro_preco", "livro_estoque"]
    prepopulated_fields = {"livro_slug": ("livro_nome", "livro_autor")}


@admin.register(ProdutoEstoque)
class ProdutoEstoqueAdmin(admin.ModelAdmin):
    list_display = (
        "movimentado_em",
        "produto",
        "quantidade",
        "movimentado_por",
    )

    raw_id_fields = ("produto", "movimentado_por")
    readonly_fields = ("movimentado_por",)

    def save_model(self, request, obj, form, change):
        obj.movimentado_por = request.user
        super().save_model(request, obj, form, change)
