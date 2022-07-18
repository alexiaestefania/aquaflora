from enum import auto, unique
from tabnanny import verbose
from crum import get_current_user

from django.db import models
from django.db.models import Sum
from django.db.models.base import Model
from django.db.models.deletion import PROTECT
from django.conf import settings
from django.db.models.fields.related import ForeignKey
from django.utils import tree
from django.urls import reverse

# para coisas que eut enho que editar depois, pesquisar por FINDHERE


# -------------------------classes de gerenciamento


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(livro_ativo=True)


# -------------------classes de estoque


class Categoria(models.Model):
    cat_nome = models.CharField(verbose_name="Categoria", max_length=255, db_index=True)
    cat_slug = models.SlugField(max_length=255, unique=True)
    cat_ativa = models.BooleanField(verbose_name="Ativo", default=True, help_text="Marque como falso caso queira arquivar a categoria.")
    cat_criadoem = models.DateTimeField(
        verbose_name="Criado em:", auto_now_add=True, editable=False
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="criador_categoria",
        on_delete=models.PROTECT,
        editable=False,
        null=True,
    )  # chave estrangeira para colaboradores q podem criar produto, em deleta protege o produto de ser deletado

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(Categoria, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("aquaflorastore:categoriaview", args=[self.cat_slug])

    def __str__(self):
        return self.cat_nome  # para retornar o nome da categoria em procura


class Produto(models.Model):
    livro_nome = models.CharField(verbose_name="Nome do livro", max_length=255)
    livro_autor = models.CharField(verbose_name="Autor do Livro", max_length=255)
    livro_desc = models.TextField(verbose_name="Descrição", blank=True)
    livro_editora = models.CharField(verbose_name="Editora", max_length=255)
    livro_ano = models.CharField(verbose_name="Ano", max_length=255)
    livro_idioma = models.CharField(verbose_name="Idioma", max_length=255)
    livro_acab = models.CharField(verbose_name="Acabamento", max_length=255)
    img_1 = models.ImageField(upload_to="images/", default="images/Default01.jpg")
    livro_preco = models.DecimalField(
        verbose_name="Preço",
        max_digits=6,
        decimal_places=2,
        help_text="Considere as taxas do Mercado Pago sobre pagamentos ao estabelecer o preço."
    )
    livro_slug = models.SlugField(max_length=255)
    livro_ativo = models.BooleanField(verbose_name="Ativo", default=True, help_text="Marque como falso caso queira arquivar esse produto.")
    livro_estoque = models.BooleanField(verbose_name="Em Estoque", default=True)
    livro_BS = models.BooleanField(verbose_name="Popular/Mais Vendido", default=False, help_text="Marque essa opção como verdadeira de acordo com os relatórios de vendas.")
    livro_NEW = models.BooleanField(verbose_name="Lançamento", default=False)
    livro_PROMO = models.BooleanField(verbose_name="Promoção", default=False)
    livro_criadoem = models.DateTimeField(verbose_name="Criado em:", auto_now_add=True)
    livro_atualizadoem = models.DateTimeField(
        verbose_name="Atualizado em:", auto_now=True
    )
    objects = models.Manager()
    produtos = ProductManager()
    Categoria = models.ForeignKey(
        Categoria, related_name="Produto", on_delete=models.CASCADE
    )  
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="criador_produto",
        on_delete=models.PROTECT,
        editable=False,
        null=True,
    )

    class Meta:
        ordering = (
            "-livro_criadoem",
        ) 

        verbose_name = "Livro"

    @property
    def livro_qtdd(self):
        return self.produtoestoque_set.aggregate(qtd=Sum("quantidade"))["qtd"]

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(Produto, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("aquaflorastore:product_detail", args=[self.livro_slug])

    def __str__(self):
        return self.livro_nome


class ProdutoEstoque(models.Model):
    produto = models.ForeignKey(
        "Produto", verbose_name="produto", on_delete=models.CASCADE
    )
    movimentado_em = models.DateTimeField(auto_now=True)
    movimentado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="movimentado_por",
        on_delete=models.CASCADE,
    )
    quantidade = models.IntegerField(verbose_name="quantidade", default=0, help_text="Importante: Ao retirar exemplares do estoque, utilize números negativos. Ao adicionar exemplares, utilize números positivos.")

    class Meta:
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"

    def __str__(self):
        return f"{self.produto} {self.quantidade}"
