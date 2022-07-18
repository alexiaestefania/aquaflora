import requests
from datetime import timedelta
from django.http.response import HttpResponseRedirect
from django.utils import timezone
from requests.structures import CaseInsensitiveDict
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.conf import settings

from .models import Pedido, ItemPedido

mercadopagokey = (
    "TEST-4558393011090479-011006-b46b4fa5512e81d1c0ad428d3b5a9609-174574759"
)


@login_required
def pagina_pedidos_auth(request):
    UserPedidos = Pedido.objects.filter(user=request.user)
    if not UserPedidos.exists():
        return render(request, "pedido/none.html")

    for pedido in UserPedidos:
        
        if pedido.payment_id == 'Unknown':
            
            pass
        elif pedido.precisa_consultar_mercado_pago():
                pedido.consultar_estado_no_mercado_pago()

    return render(
        request,
        "pedido/pedidos.html",
        {
            "pedidos": UserPedidos,
        },
    )

@login_required
def cancelar_pedido(request, id):
    pedido = Pedido.objects.get(pk=id, user=request.user)
    # payment not APRV, just mark as CANC

    if pedido.statuspgto == Pedido.PAGAMENTO_PENDENTE:
        pedido.statuspgto = "CANC"
        pedido.statusentrega = "CANC"
        pedido.save()
        return render(request, "pedido/cancelado.html")

    elif (
        pedido.statuspgto == Pedido.PAGAMENTO_APROVADO
        and pedido.statusentrega == "PROC"
    ):
        # figure out hwo to send a request to mercado pago probably.
        #right now it works manually. staff must cancel order then mark accordingly.
        pedido.statuspgto = "CANP"
        pedido.statusentrega = "CANC"
        pedido.save()
        return render(request, "pedido/cancelado.html", {"id": id})

    elif (
        pedido.statuspgto == Pedido.PAGAMENTO_APROVADO
        and pedido.statusentrega == "ENCM"
    ):
        return render(request, "pedido/cancelamento_help.html")

    elif (
        pedido.statuspgto == Pedido.PAGAMENTO_APROVADO
        and pedido.statusentrega == "ENTR"
    ):
        end_date = timezone.now()
        start_date = pedido.criadoem
        if end_date - start_date > timedelta(days=7):
            return render(request, "pedido/devolucoes_help.html")
        else:
            return render(request, "pedido/norefunds_help.html")
    else:
        return render(request, "pedido/falha_cancelamento.html")

@login_required
def pagar_pedido(request, id):
    pedido = Pedido.objects.get(pk=id, user=request.user)
    # make sre this is PENDING
    if pedido.statuspgto != Pedido.PAGAMENTO_PENDENTE:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    preference_id = pedido.preference_id
    
    return render(request, "checkout/metodopagto.html", {
         "preference_id": preference_id,
         'pedidoid' : pedido.id}
    )

     

    
    


# USEFU LREFERENCES


# payment status response dict will contain
#   "id": 1,
#   "date_created": "2017-08-31T11:26:38.000Z",
#   "date_approved": "2017-08-31T11:26:38.000Z",
#   "date_last_updated": "2017-08-31T11:26:38.000Z",
#   "money_release_date": "2017-09-14T11:26:38.000Z",
#   "payment_method_id": "account_money",
#   "payment_type_id": "credit_card",
#   "status": "approved",
#   "status_detail": "accredited",
#   "currency_id": "BRL",
#   "description": "Pago Pizza",
#   "collector_id": 2,
#   "payer":
#     "email": "afriend@gmail.com",
#   "metadata": {},
#   "additional_info": {},
#   "order": {},
#   "transaction_amount": 250,
#   "transaction_amount_refunded": 0,
#   "coupon_amount": 0,
#   "transaction_details": {
#     "net_received_amount": 250,
#     "total_paid_amount": 250,
#     "overpaid_amount": 0,
#     "installment_amount": 250
#   },
#   "installments": 1,
#   "card": {}

# reference: https://www.mercadopago.com.br/developers/en/reference/payments/_payments_id/get
