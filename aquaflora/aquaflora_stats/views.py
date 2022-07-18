
from collections import defaultdict
from datetime import timedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.utils import timezone
from pedidos.models import Pedido
from aquaflorastore.models import Produto, ProdutoEstoque
from .forms import DatepickerForm
from django.contrib.auth.models import Group 

@staff_member_required
def Estoquereport(request):
    if request.user not in Group.objects.get(name='Gerente').user_set.all():
        return render(request, 'admin/permissionerror.html')
    if request.method == 'POST':
        dateform = DatepickerForm(request.POST)
        if dateform.is_valid():
            start_date =  dateform.cleaned_data['start_date']
            end_date = dateform.cleaned_data['end_date']
    else:
        end_date = timezone.now()
        start_date = end_date - timedelta(days=7)
        dateform = DatepickerForm()
        
    all_produtos = Produto.objects.all()
    
    all_movimentacoes_estoque = ProdutoEstoque.objects.filter(movimentado_em__range=(start_date, end_date))
    
    produtos_filtered = []
    
    for move in all_movimentacoes_estoque:
        for prod in all_produtos:
            if move.produto == prod:
                if prod not in produtos_filtered:
                    produtos_filtered.append(prod)

    print(produtos_filtered)
    entradas = defaultdict(lambda: 0)
    saidas = defaultdict(lambda: 0)
    for produto in all_produtos:
        for movs in all_movimentacoes_estoque:
            if produto.id == movs.produto.id:
                if movs.quantidade > 0:
                    entradas[produto.id] += movs.quantidade
                if movs.quantidade < 0:
                    saidas[produto.id] -= movs.quantidade                
    
    context_data = {
        'start_date' : start_date,
        'end_date' : end_date,
        'dateform' : dateform,
        'lista_produtos' : produtos_filtered,
        'lista_movimentacoes_estoque' : all_movimentacoes_estoque,
        'entradas' : entradas.items(),
        'saidas' : saidas.items(),
    }
    return render (request, 'admin/reports/estoque.html', context_data)



@staff_member_required
def FinanceiroReport(request):
    if request.user not in Group.objects.get(name='Gerente').user_set.all():
        return render(request, 'admin/permissionerror.html')
    if request.method == 'POST':
        dateform = DatepickerForm(request.POST)
        if dateform.is_valid():
            start_date =  dateform.cleaned_data['start_date']
            end_date = dateform.cleaned_data['end_date']
    else:
        end_date = timezone.now()
        start_date = end_date - timedelta(days=7)
        dateform = DatepickerForm()
    print('AFTER IF COMPLETE. START DATE IS:')
    print(start_date)
    print('END DATE IS:')
    print(end_date)
    
    #DADOS DE VENDAS E FRETE
    Vendas = Pedido.objects.filter(criadoem__range=(start_date,end_date), statuspgto='APRV', statusentrega='ENTR')
    num_vendas = Vendas.count()
    
    vendas_bruto, vendas_liquido, gastos_frete = 0,0,0
    print("¨¨¨¨¨¨¨¨¨¨¨¨GET VENDAS ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨")
    
    for venda in Vendas:
        print(venda)
        vendas_bruto += venda.valorpgto
        gastos_frete += venda.userFrete.FretePreco
        
    #DADOS DE DESPESAS
    
    Estornos = Pedido.objects.filter(criadoem__range=(start_date,end_date), statuspgto='ESTR')
    Estravios = Pedido.objects.filter(criadoem__range=(start_date,end_date), statusentrega='ESTR')
    Devolucoes = Pedido.objects.filter(criadoem__range=(start_date,end_date), statusentrega='DEVV')
    
    desp_estorno, desp_estravios, desp_devos = 0,0,0
    
    for i in Estornos:
        desp_estorno += i.valorpgto
    
    for i in Estravios:
        desp_estravios += i.valorpgto
        
    for i in Devolucoes:
        desp_devos += i.valorpgto
        
    #PEDIDOS ENCAMINHADOS
    Encaminhados = Pedido.objects.filter(criadoem__range=(start_date,end_date), statusentrega='ENCM')
    vendas_previstas = 0
    for i in  Encaminhados:
        vendas_previstas += i.valorpgto

    contagem_previstas = Encaminhados.count()
    
    #VAIAVEIS TRATADAS
    vendas_liquido = vendas_bruto - gastos_frete
    gastos_estravios = desp_estorno + desp_estravios + desp_devos
    despesas_totais = gastos_estravios + gastos_frete
    lucro_total = vendas_liquido - despesas_totais
    
    contextdata = {
        'dateform' : dateform,
        'start_date' : start_date,
        'end_date' : end_date,
        'Vendas' : Vendas,
        'num_vendas' : num_vendas,
        'vendas_previstas' : vendas_previstas,
        'contagem_previstas' : contagem_previstas,
        'vendas_bruto' : vendas_bruto,
        'vendas_liquido' : vendas_liquido,
        'gastos_estravios' :gastos_estravios,
        'gastos_frete' : gastos_frete,
        'despesas_totais' : despesas_totais,
        'lucro_total' : lucro_total,
    }
    return render (request, 'admin/reports/financeiro.html', contextdata)


@staff_member_required
def BestSeller(request):
    if request.user not in Group.objects.get(name='Gerente').user_set.all():
        return render(request, 'admin/permissionerror.html')    
    if request.method == 'POST':
        dateform = DatepickerForm(request.POST)
        if dateform.is_valid():
            start_date =  dateform.cleaned_data['start_date']
            end_date = dateform.cleaned_data['end_date']
    else:
        end_date = timezone.now()
        start_date = end_date - timedelta(days=7)
        dateform = DatepickerForm()

    
    pedidos = Pedido.objects.filter(criadoem__range=(start_date,end_date), statuspgto='APRV')
    #pega pedidos com pagamento aprovado dentro das datas corretas
    num_pedidos = pedidos.count()
    
    livros = []
    for pedido in pedidos:
        for item in pedido.Itens.all():
            livros.append(item)
    
    por_popularidade = defaultdict(lambda: 0)
    for livro in livros:
        por_popularidade[livro.produto.livro_nome] += int(livro.qtdd)   


    contextdata = {
            'livros' : livros,
            'num_pedidos' : num_pedidos,
            'start_date' : start_date,
            'end_date' : end_date,
            'dateform' : dateform,
            'por_popularidade':por_popularidade.items(),
            }
    return render (request, 'admin/reports/maisvendidos.html', contextdata)

