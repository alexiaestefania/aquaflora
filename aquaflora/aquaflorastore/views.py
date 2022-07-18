from django.shortcuts import render, get_object_or_404
from .models import Categoria, Produto
from .forms import SearchForm

def search(request):
    form = SearchForm(request.GET or None)
    
    results = Produto.objects.all()
    
    if form.is_valid():
        results = form.filter_results(results)
    return render(request, 'search/search_results.html', {'query': results})

def allproducts(request):
    
    produtosativos = Produto.objects.filter(livro_estoque=True, livro_ativo=True) 
    produtosvalidos = (x for x in produtosativos if x.livro_qtdd > 0)
     
    return render(request, 'home.html', {'produtos': produtosvalidos})

def product_detail(request, livro_slug):
    product = get_object_or_404(Produto, livro_slug=livro_slug, livro_estoque=True, livro_ativo=True)
    qtddrange = product.livro_qtdd
    return render(request, 'prodview.html', {'product': product, 'qtddrange':range(1, qtddrange)})

def categoriaview(request, cat_slug):
    categoria = get_object_or_404(Categoria, cat_slug=cat_slug)
    produtos = Produto.objects.filter(Categoria = categoria, livro_estoque=True, livro_ativo=True)
    return render(request, 'category.html', {'categoria': categoria, 'produtos': produtos})
    
def lancamentos(request):
    produtos = Produto.objects.filter(livro_NEW=True, livro_ativo=True)
    return render(request, 'lancamentos.html', {'produtos': produtos})        

def promo(request):
    produtos = Produto.objects.filter(livro_PROMO=True, livro_ativo=True)
    return render(request, 'promocoes.html', {'produtos': produtos})    

def bestseller(request):
    produtos = Produto.objects.filter(livro_BS=True, livro_ativo=True)
    return render(request, 'bestsellers.html', {'produtos': produtos})    

def samplepage(request):
     return render(request, 'contact.html')