from .models import Categoria
from .forms import SearchForm

def categorias(request):
    return {
        'categorias': Categoria.objects.all()
    }
    
def search(request):
    form = SearchForm(request.GET or None)
    searchcontext = {
        'searchform' : form
    }
    return searchcontext