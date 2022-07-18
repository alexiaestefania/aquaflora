from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import UserCliente, UserEndereco

#---------------------------------------------- LOGIN

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Endereço de e-mail', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Senha',
            'id': 'login-pwd',
        }
    ))
    
#---------------------------------------------- CRIAR CONTA

class RegistrationForm(forms.ModelForm):

    username = forms.CharField(label='Escolha um nome de usuário', min_length=4, max_length=35, help_text='Obrigatório.')
    
    email = forms.EmailField(label='Seu endereço de e-mail', max_length=200, help_text='Obrigatório.', error_messages={'required': 'Um endereço de e-mail válido é necessário.'})
    
    password = forms.CharField(label='Sua Senha', widget=forms.PasswordInput)
    
    password2 = forms.CharField(label='Repita a Senha', widget=forms.PasswordInput)

    class Meta:
        model = UserCliente
        fields = ('username', 'email',)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        cu = UserCliente.objects.filter(username=username)
        if cu.count():
            raise forms.ValidationError("Este nome de usuário já está cadastrado.")
        return username

    def clean_password2(self):
        cp = self.cleaned_data
        if cp['password'] != cp['password2']:
            raise forms.ValidationError('As senhas não são iguais.')
        return cp['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserCliente.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Este endereço de e-mail já está cadastrado.')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Nome de usuário'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': ''})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})
    
#---------------------------------------------- EDITAR CONTA

class UserEditForm(forms.ModelForm):
    class Meta:
        model = UserCliente
        fields = (
            'email',
            'username',
            'nome',
            'tel'
            )
    
    email = forms.EmailField(label='Endereço de E-mail (não pode ser trocado)', max_length=200, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))
    
    username = forms.CharField(label='Nome de Usuário (não pode ser trocado)', min_length=4, max_length=35, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-username', 'readonly': 'readonly'}))
    
    nome = forms.CharField(
        label='Nome Completo', max_length=255, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Seu nome completo.', 'id': 'form-nome'}))
    
    tel = forms.CharField(
        label='Seu número de telefone', max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Telefone', 'id': 'form-tel'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['email'].required = True

    
#---------------------------------------------- ADD ENDERECO
class UserEnderecoForm(forms.ModelForm):
    class Meta:
        model = UserEndereco
        fields = (
            'en_nomecompleto',
            'en_tel',
            'en_cep',
            'en_rua',
            'en_bairro',
            'en_cidade',
            'en_estado',
            'en_compl'
        )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['en_nomecompleto'].widget.attrs.update({'class' : 'form-control mb-2 account-form', 'placeholder': 'Nome Completo do Destinatário'})
        
        self.fields["en_tel"].widget.attrs.update({'class' : 'form-control mb-2 account-form', 'placeholder' : 'Telefone para contato', 'id' : 'en_tel'})
        
        self.fields["en_cep"].widget.attrs.update({'class' : 'form-control mb-2 account-form', 'id' : 'en_cep', 'onchange' : 'getaddress()'})
        
        self.fields["en_rua"].widget.attrs.update({'class' : 'form-control mb-2 account-form', 'placeholder' : 'Logradouro', 'id' : 'en_rua'})
        
        self.fields["en_bairro"].widget.attrs.update({'class' : 'form-control mb-2 account-form', 'placeholder' : 'Bairro ou Vizinhança', 'id' : 'en_bairro'})
        
        self.fields["en_cidade"].widget.attrs.update({'class' : 'form-control mb-2 account-form', 'placeholder' : 'Cidade', 'id' : 'en_cidade'})
        
        self.fields["en_estado"].widget.attrs.update({'class' : 'form-control mb-2 account-form', 'id' : 'en_estado'})
        
        self.fields["en_compl"].widget.attrs.update({'class' : 'form-control mb-2 account-form', 'placeholder' : 'Complemento (Ex: número de apartamento, bloco, etc.)'})
        
        
#---------------------------------------------- EDIT ENDERECO
class EditUserEnderecoForm(forms.ModelForm):
    class Meta:
        model = UserEndereco
        fields = (
            'en_nomecompleto',
            'en_tel',
            'en_cep',
            'en_rua',
            'en_bairro',
            'en_cidade',
            'en_estado',
            'en_compl'
        )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['en_nomecompleto'].widget.attrs.update({'class' : 'form-control mb-2 account-form', 'id' : 'en_nomecompleto'})
        
        self.fields["en_tel"].widget.attrs.update({'class' : 'form-control mb-2 account-form', 'id' : 'en_tel'})
        
        self.fields["en_cep"].widget.attrs.update({'class' : 'form-control mb-2 account-form', 'id' : 'en_cep', 'onchange' : 'getaddress()', })
        
        self.fields["en_rua"].widget.attrs.update({'class' : 'form-control mb-2 account-form', 'id' : 'en_rua'})
        
        self.fields["en_bairro"].widget.attrs.update({'class' : 'form-control mb-2 account-form', 'id' : 'en_bairro'})
        
        self.fields["en_cidade"].widget.attrs.update({'class' : 'form-control mb-2 account-form', 'id' : 'en_cidade'})
        
        self.fields["en_estado"].widget.attrs.update({'class' : 'form-control mb-2 account-form', 'id' : 'en_estado'})
        
        self.fields["en_compl"].widget.attrs.update({'class' : 'form-control mb-2 account-form'})