from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .carrinho import Carrinho
from aquaflorastore.models import Produto

def carrinhoresumo(request):
    carrinho = Carrinho(request)
    empty = False
    carrinhototal = carrinho.gettotal()
    if carrinhototal == 0:
        empty = True
    qtyrange = 10
    return render(request, 'carrinho/carrinho.html', {'carrinho' : carrinho, 'empty' : empty, 'qtyrange':range(1, qtyrange)})
  

def carrinho_add(request):
    carrinho = Carrinho(request)
    produto_id = int(request.POST.get('produtoid'))
    
    if request.POST.get('action') == 'post':
        produto_qty = int(request.POST.get('produtoqty'))
        produto = get_object_or_404(Produto, id=produto_id)
        carrinho.add(produto=produto, qty=produto_qty)
        cartqty = carrinho.__len__()
        response = JsonResponse({'qty':cartqty })
        return response
    
    if request.POST.get('action') == 'del':
        carrinho.delete(produto=produto_id)
        cartqty = carrinho.__len__()
        carrinhototal = carrinho.gettotal()
        response = JsonResponse({'qty': cartqty, 'subtotal': carrinhototal})
        return response
        
    if request.POST.get('action') == 'quickpost':
        produto = get_object_or_404(Produto, id=produto_id)
        carrinho.quickadd(produto=produto, qty=1)
        cartqty = carrinho.__len__()
        response = JsonResponse({'qty':cartqty })
        return response
    
    if request.POST.get('action') == 'update':
        produto_qty = int(request.POST.get('produtoqty'))
        carrinho.update(produto=produto_id, qty=produto_qty)
        cartqty = carrinho.__len__()
        carrinhototal = carrinho.gettotal()
        response = JsonResponse({'qty': cartqty, 'subtotal': carrinhototal})
        return response