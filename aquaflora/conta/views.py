from django.shortcuts import redirect, render
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.forms.models import model_to_dict
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.urls import reverse

from .token import account_activation_token
from .forms import (
    RegistrationForm,
    UserEditForm,
    UserEnderecoForm,
    EditUserEnderecoForm,
)
from .models import UserCliente, UserEndereco

# =====================================


# ----------------------
# classes de reditect


@login_required
def loginredirect(request):
    enderecos = UserEndereco.objects.filter(user=request.user)
    return redirect("conta:perfil")


# ----------------------
# classes de perfil


@login_required
def perfil(request):
    if request.user.is_authenticated:
        enderecos = UserEndereco.objects.filter(user=request.user)
        return render(request, "conta/perfil.html", {"enderecos": enderecos})
    else:
        return redirect("conta:registar")


@login_required
def editar_perfil(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()

    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, "conta/editarperfil.html", {"user_form": user_form})


@login_required
def excluir_perfil(request):
    user = UserCliente.objects.get(username=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect("conta:delete_confirmation")


# ----------------------
# classe para criacao de conta


def criar_conta(request):

    if request.user.is_authenticated:
        return redirect("conta:perfil")

    if request.method == "POST":
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = "Ative sua Conta na Livraria Aquaflora"
            message = render_to_string(
                "conta/registro/email_ativacao.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            return render(request, "conta/registro/sucesso.html")
    else:
        registerForm = RegistrationForm()
    return render(request, "conta/registro/signup.html", {"form": registerForm})


# ----------------------
# classe para ativacao da conta via link no email


def ativar_conta(
    request, uidb64, token, backend="django.contrib.auth.backends.ModelBackend"
):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserCliente.objects.get(pk=uid)
    except:
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("conta:perfil")
    else:
        return render(request, "conta/registro/ativacao_invalida.html")


# ----------------------
# classes de endereço


@login_required
def enderecos(request):
    enderecos = UserEndereco.objects.filter(user=request.user)
    return render(request, "conta/perfil_enderecos.html", {"enderecos": enderecos})


@login_required
def enderecos_add(request):
    address_form = UserEnderecoForm(request.POST or None)
    if address_form.is_valid():
        data = address_form.save(commit=False)
        data.user = request.user
        data.save()
        return redirect(reverse("conta:enderecos"))

    # if request.method == 'POST':
    #     address_form = UserEnderecoForm(data=request.POST)
    #     if address_form.is_valid():
    #         address_form = address_form.save(commit=False)
    #         address_form.user = request.user
    #         address_form = address_form.save()
    #         return HttpResponseRedirect(reverse("conta:enderecos"))
    #     else:
    #         address_form = UserEnderecoForm()
    return render(request, "conta/perfil_addender.html", {"form": address_form})


@login_required
def enderecos_edit(request, id):
    ender = UserEndereco.objects.get(pk=id, user=request.user)
    ender_dict = model_to_dict(ender)
    if request.method == "POST":
        address_form = EditUserEnderecoForm(instance=ender, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("conta:enderecos"))
    else:
        address_form = EditUserEnderecoForm(instance=ender, data=request.POST)
    return render(
        request,
        "conta/perfil_editender.html",
        {"form": EditUserEnderecoForm, "ender": ender},
    )


@login_required
def enderecos_del(request, id):
    ender = UserEndereco.objects.filter(pk=id, user=request.user).delete()
    return redirect("conta:enderecos")


@login_required
def enderecos_default(request, id):
    UserEndereco.objects.filter(user=request.user, default=True).update(default=False)
    UserEndereco.objects.filter(pk=id, user=request.user).update(default=True)
    previous_url = request.META.get("HTTP_REFERER")
    if "checkout" in previous_url:
        return redirect("checkout:paginacheckout")
    else:
        return redirect("conta:enderecos")


@login_required
def perfilpedidos(request):
    return render(request, "conta/perfil_pedidos.html")
