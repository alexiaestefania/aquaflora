from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import User_Wishlist
from aquaflorastore.models import Produto

@login_required
def wishlist(request):
    if request.user.is_authenticated:
        wishlist = User_Wishlist.objects.filter(user=request.user)
        return render(request, "conta/perfil.html", { 'wishlist': wishlist })
    else:
        return redirect("conta:registar")
    
@login_required 
def wishlist_add(request, produto_id):
    produto = Produto.objects.get(pk=produto_id)
    user = request.user
    
    return