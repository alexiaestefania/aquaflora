
import json
from email.policy import HTTP
from urllib.request import HTTPRedirectHandler
from decouple import config
import requests
from carrinho.carrinho import Carrinho
from conta.models import UserEndereco
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import (HttpResponseRedirect, JsonResponse)
from django.shortcuts import redirect, render

from django.urls import reverse
from pedidos.models import ItemPedido, Pedido

import mercadopago

from .models import OpcoesFrete

token = config('ACCESS_TOKEN_MP')

sdk = mercadopago.SDK(token) 

@login_required
def paginacheckout(request):
    opcoesfrete = OpcoesFrete.objects.filter(Frete_Ativo=True)
    enderecos = UserEndereco.objects.filter(user=request.user).order_by("-default")
    carrinho = Carrinho(request)
    empty = False
    carrinhototal = carrinho.gettotal()
    if carrinhototal == 0:
        empty = True
    return render(request, "checkout/checkout.html", {'opcoesfrete' : opcoesfrete, 'enderecos' : enderecos, 'empty' : empty})

@login_required
def updatefrete(request):
    carrinho = Carrinho(request)
    if request.POST.get("action") == "post":
        delivery_option = int(request.POST.get("deliveryOption"))
        delivery_type = OpcoesFrete.objects.get(id=delivery_option)
        total_updated = carrinho.updatefrete(delivery_type.FretePreco)
        session = request.session
        if 'compra' not in request.session:
            session['compra'] = {
                'delivery_id': delivery_type.id
            }
            session.modified = True
        else:
            session['compra']['delivery_id'] = delivery_type.id
            session.modified = True
            
    response = JsonResponse({'total': total_updated, 'FretePreco' : delivery_type.FretePreco})
    return response


@login_required
def pagamento(request):
    
    session = request.session
    
    if 'compra' not in request.session:
        messages.success(request, "Por favor selecione seu frete antes de prosseguir com pagamento.")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        carrinho = Carrinho(request)
        if carrinho:
            Cliente = request.user
            userFreteID = session['compra']['delivery_id']
            enderecos = UserEndereco.objects.filter(user=Cliente)
            for i in enderecos:
                if i.default:
                    endereco = i
            delivery_type = OpcoesFrete.objects.get(id=userFreteID)
            total_updated = carrinho.updatefrete(delivery_type.FretePreco)
            pedido = Pedido.objects.create(
                user = Cliente,
                valorpgto = total_updated,
                userEnderecoEntrega = endereco,
                userFrete = delivery_type,
                preference_id = 'processing'
            )
            items_in_pedido = []
            for item in carrinho:
                items_in_pedido.append(ItemPedido.objects.create(
                    pedidoID = pedido,
                    produto = item["produto"],
                    qtdd = item["qty"],
                    preco = item["preco"],
                ))
            
            cartqty = carrinho.__len__()
            valortotal = str(total_updated)
            pedidoid = str(pedido)
            clientmail = Cliente.email
            fretevalor = float(delivery_type.FretePreco)
            preference_data = {
                "title": "Aquaflora - Pedido" + pedidoid,
                "quantity": cartqty,
                "currency_id": "BRL",
                "unit_price": valortotal,
                "items": [i.to_mercado_pago_item_list() for i in items_in_pedido],
                "payer": {
                    "email": clientmail,
                },
                "shipments":{
                    "cost": fretevalor,
                    "mode": "not_specified",
                },
                "back_urls": {
                    "success": 'http://127.0.0.1:8000/checkout/status',
                    "failure": 'http://127.0.0.1:8000/checkout/status',
                    "pending": 'http://127.0.0.1:8000/checkout/status'
                },
                "auto_return": "all",
                "statement_descriptor": "AquafloraLivros"
            }
            preference_response = sdk.preference().create(preference_data)
            preference = preference_response["response"]
            
            if 'error' in preference:
                print('\n-------------------------------\nERRO NA PREFERENCIA FAVOR REVISAR: VEJA ABAIXO\n' + preference + '\n----------------------------------')
            preference_id = preference["id"]
            Pedido.objects.filter(id=pedidoid).update(
                preference_id = preference_id
            )
            return render(request, "checkout/metodopagto.html", {"preference_id": preference_id, 'pedidoid' : pedidoid})
        else:
            return HttpResponseRedirect(request.META["HTTP_REFERER"])

@login_required
def pagamento_status(request):
    
    # collection_id= 1248028804
    # collection_status= approved
    # payment_id= 1248028804
    # status= approved
    # external_reference= null
    # payment_type= credit_card
    # merchant_order_id= 4727585412
    # preference_id= 174574759-9c32f2a6-18a6-4ecf-afaf-ac8ecc438e6a
    # site_id= MLB
    # processing_mode= aggregator
    # merchant_account_id= null
    
        # Payment status
        # pending: The user has not yet completed the payment process.
        # approved: The payment has been approved and accredited.
        # authorized: The payment has been authorized but not captured yet.
        # in_process: Payment is being reviewed.
        # in_mediation: Users have initiated a dispute.
        # rejected: Payment was rejected. The user may retry payment.
        # cancelled: Payment was cancelled by one of the parties or because time for payment has expired
        # refunded: Payment was refunded to the user.
        # charged_back: A chargeback was made in the buyer’s credit card.
    
    mercado_pago_params = request.GET.dict()
    pedido = Pedido.objects.filter(preference_id=request.GET.get('preference_id'))
    
    pedido.update(
        payment_id = mercado_pago_params['payment_id']
        )
    carrinho = Carrinho(request)
    if mercado_pago_params['status'] == 'approved':
        pedido.update(
            statuspgto = Pedido.PAGAMENTO_APROVADO
            )
        carrinho.clear()
        return render(request, "checkout/payment_success.html")
    elif mercado_pago_params['status'] == 'pending' or mercado_pago_params['status'] == 'authorized' or mercado_pago_params['status'] == 'in_process':
        pedido.update(
            statuspgto = Pedido.PAGAMENTO_PENDENTE
            )
        carrinho.clear()
        return render(request, "checkout/payment_pending.html")
    
    elif mercado_pago_params['status'] == 'rejected':
        pedido.update(
            statuspgto = Pedido.PAGAMENTO_REJEITADO
        )
        return render(request, "checkout/payment_rejected.html")
        
    elif mercado_pago_params['status'] == 'cancelled':
        pedido.update(
            statuspgto = Pedido.PAGAMENTO_CANCELADO
        )
        return render(request, "checkout/payment_canceled.html")
    
    elif mercado_pago_params['status'] == 'refunded' or mercado_pago_params['status'] == 'charged_back':
        pedido.update(
            statuspgto = Pedido.PAGAMENTO_ESTORNADO
        )
        return render(request, "checkout/payment_refunded.html")
    
    elif mercado_pago_params['status'] == 'in_mediation':
        pedido.update(
            statuspgto = Pedido.PAGAMENTO_DISPUTA
        )
        return render(request, "checkout/payment_dispute.html")
    else:
        return redirect(reverse('allproducts'))



#----------------------VIEWS PARA COMPRS EXPRESSA

""" 
def checkoutexpress(request):
    opcoesfrete = OpcoesFrete.objects.filter(Frete_Ativo=True)
    enderecos = 'placeholder' #criar um form com nome, cpf, endereco, e telefone obrigatorios
    carrinho = Carrinho(request)
    empty = False
    carrinhototal = carrinho.gettotal()
    if carrinhototal == 0:
        empty = True
    return render(request, "checkout/checkout.html", {'opcoesfrete' : opcoesfrete, 'enderecos' : enderecos, 'empty' : empty})

def pagamentoexpress(request):
    session = request.session
    if 'compra' not in request.session:
        messages.success(request, "Por favor selecione seu frete antes de prosseguir com pagamento.")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        carrinho = Carrinho(request)
        if carrinho:
            userFreteID = session['compra']['delivery_id']
            endereco = 'placeholder' #add info to session?
            delivery_type = OpcoesFrete.objects.get(id=userFreteID)
            total_updated = carrinho.updatefrete(delivery_type.FretePreco)
            pedido = Pedido.objects.create(
                valorpgto = total_updated,
                userEnderecoEntrega = endereco,
                userFrete = delivery_type,
            )
            items_in_pedido = []
            for item in carrinho:
                items_in_pedido.append(ItemPedido.objects.create(
                    pedidoID = pedido,
                    produto = item["produto"],
                    qtdd = item["qty"],
                    preco = item["preco"],
                ))
            
            cartqty = carrinho.__len__()
            valortotal = str(total_updated)
            pedidoid = str(pedido)
            clientmail = 'get email and cpf via form along w address'
            preference_data = {
                "title": "Aquaflora - Pedido" + pedidoid,
                "quantity": cartqty,
                "currency_id": "BRL",
                "unit_price": valortotal,
                "items": [i.to_mercado_pago_item_list() for i in items_in_pedido],
                "payer": {
                    "email": clientmail,
                }
            }
            preference_response = sdk.preference().create(preference_data)
            preference = preference_response["response"]   
            preference_id = preference["id"]
            carrinho.clear()
            return render(request, "checkout/metodopagto.html", {"preference_id": preference_id, 'pedidoid' : pedidoid})
        else:
            return HttpResponseRedirect(request.META["HTTP_REFERER"])
"""