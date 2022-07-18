from datetime import timedelta
from django.db import models
from django.conf import settings
import requests
from requests.structures import CaseInsensitiveDict
from aquaflorastore.models import Produto
from conta.models import UserEndereco
from aquaflora_checkout.models import OpcoesFrete
from django.conf import settings
from django.utils import timezone


class Pedido(models.Model):
    PAGAMENTO_APROVADO = "APRV"
    PAGAMENTO_PENDENTE = "PEND"
    PAGAMENTO_CANCELADO = "CANC"
    PAGAMENTO_ESTORNO_PROCESSAMENTO = "CANP"
    PAGAMENTO_REJEITADO = "REJC"
    PAGAMENTO_ESTORNADO = "ESTR"
    PAGAMENTO_DISPUTA = "DISP"
    
    PAGTO = (
        (PAGAMENTO_APROVADO, "Pagamento Aprovado"),
        (PAGAMENTO_PENDENTE, "Pagamento Pendente"),
        (PAGAMENTO_CANCELADO, "Pedido Cancelado Antes de Pagar"),
        (PAGAMENTO_ESTORNO_PROCESSAMENTO, "Estorno em Processamento"),
        (PAGAMENTO_REJEITADO, "Estornado"),
        (PAGAMENTO_ESTORNADO, "Rejeitado"),
        (PAGAMENTO_DISPUTA, "Disputado"),
    )

    ESTADOS_MERCADO_PAGO = {
        "approved": PAGAMENTO_APROVADO,
        "pending": PAGAMENTO_PENDENTE,
        "authorized": PAGAMENTO_PENDENTE,
        "in_process": PAGAMENTO_PENDENTE,
        "rejected": PAGAMENTO_REJEITADO,
        "cancelled": PAGAMENTO_CANCELADO,
        "in_mediation": PAGAMENTO_DISPUTA,
    }
    
    ESTADOS_MERCADO_PAGO_FINALIZADOS = (
        PAGAMENTO_APROVADO,
        PAGAMENTO_CANCELADO,
        PAGAMENTO_ESTORNADO,
        PAGAMENTO_REJEITADO,
    )

    ENTRG = (
        ("PROC", "Processando Pedido"),
        ("ENCM", "Pacote Encaminhado"),
        ("ENTR", "Pacote Entregue"),
        ("DEVV", "Pacote Devolvido"),
        ("ESTR", "Pacote Estraviado"),
        ("CANC", "Pedido Cancelado Antes de Enviar"),
    )
    # FIXME não pode Unknown. Talvez aceitar como string vazia para permitir
    # que continue o pagamento se a janela do MP for fechada.
    preference_id = models.CharField(
        max_length=255, verbose_name="ID da Preferência", blank=False, default="Unknown"
    )
    payment_id = models.CharField(
        max_length=255, verbose_name="ID do Pagamento", blank=False, default="Unknown"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="usuario_pedido",
        verbose_name="Usuário",
        blank=True,
        editable=False,
    )
    userEnderecoEntrega = models.ForeignKey(
        UserEndereco,
        on_delete=models.CASCADE,
        related_name="usuario_endereco",
        verbose_name="Endereço de Entrega",
        blank=False,
        editable=False,
    )
    userFrete = models.ForeignKey(
        OpcoesFrete,
        on_delete=models.CASCADE,
        related_name="opcao_frete",
        verbose_name="Frete Escolhido",
        blank=False,
        editable=False,
    )
    criadoem = models.DateTimeField(
        verbose_name="Criado em", auto_now_add=True, editable=False
    )
    valorpgto = models.DecimalField(
        verbose_name="Valor Total", max_digits=9, decimal_places=2, editable=False
    )
    statuspgto = models.CharField(max_length=100, choices=PAGTO, default="PEND")
    statusentrega = models.CharField(max_length=100, choices=ENTRG, default="PROC")

    class Meta:
        ordering = ("-criadoem",)
        verbose_name = "Pedido"

    def __str__(self):
        return str(self.id)

    def Destinatario(self):
        return str(self.userEnderecoEntrega.en_nomecompleto)

    def Endereco(self):
        return str(
            "CEP: "
            + self.userEnderecoEntrega.en_cep
            + ". "
            + self.userEnderecoEntrega.en_rua
            + ", "
            + self.userEnderecoEntrega.en_bairro
            + ". "
            + self.userEnderecoEntrega.en_cidade
            + " - "
            + self.userEnderecoEntrega.en_estado
            + ". "
            + self.userEnderecoEntrega.en_compl
        )

    def consultar_estado_no_mercado_pago(self) -> None:
        # sends GET request to mercado pago to obtain status data using the payment id from database
        headers = CaseInsensitiveDict()
        headers["Authorization"] = settings.ACCESS_TOKEN_MP
        url = (
            "https://api.mercadopago.com/v1/payments/" + self.payment_id
        )  # is this correct?
        r = requests.get(url, headers=headers)
        print(url)
        pagamento = r.json()
        try:
            self.statuspgto = Pedido.ESTADOS_MERCADO_PAGO[pagamento["status"]]
        except KeyError:
            raise Exception(f"Estado de pagamento desconhecido {pagamento['status']}")
        self.save()

    def precisa_consultar_mercado_pago(self) -> bool:
        # FIXME remover isso depois de tratar os payment_id do MP em Unkown
        if self.payment_id == "Unknown":
            return False
        return self.statuspgto not in self.ESTADOS_MERCADO_PAGO_FINALIZADOS

    def pode_reembolsar(self) -> bool:
        if self.statuspgto == self.PAGAMENTO_CANCELADO:
            return False
        return (timezone.now() - self.criadoem) < timedelta(
            days=settings.DAYS_FOR_REEMBOLSO
        )


class ItemPedido(models.Model):
    pedidoID = models.ForeignKey(Pedido, related_name="Itens", on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, related_name="Itens", on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=9, decimal_places=2)
    qtdd = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def to_mercado_pago_item_list(self):
        return {
            "title": self.produto.livro_nome,
            "description": self.produto.livro_desc,
            "picture_url": self.produto.img_1.url,
            "category_id": self.produto.Categoria_id,
            "quantity": self.qtdd,
            "currency_id": "BRL",
            "unit_price": float(self.preco),
        }
