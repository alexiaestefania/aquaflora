from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.core.mail import send_mail
from django.db import models
from localflavor.br.models import  BRPostalCodeField, BRStateField

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UserGerente(BaseUserManager):

    def create_superuser(self, email, username, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, password, **other_fields)

    def create_user(self, email, username, password, **other_fields):

        if not email:
            raise ValueError('Por favor providencie seu endereço de e-mail')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class UserCliente(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(verbose_name="Nome Completo", max_length=255,  blank=True)
    username = models.CharField(verbose_name="Nome de Usuário", max_length=35, unique=True)
    email = models.CharField(verbose_name="Endereço de e-mail", max_length=255, unique=True)
    tel = models.CharField(verbose_name="Número de Telefone", max_length=15, blank=True)

    #status de usuarios
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = UserGerente()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Conta"

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'aquaflora_staff@aquaflora.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.username
    
    

class UserEndereco(models.Model):
    en_nomecompleto = models.CharField(verbose_name="Nome Completo", max_length=150, blank=False)
    en_tel = models.CharField(verbose_name="Número de Telefone", max_length=15, blank=True)
    en_cep = BRPostalCodeField(verbose_name="CEP",help_text="Preencha no formato: XXXXX-XXX")
    en_rua = models.CharField(verbose_name="Rua", max_length=255,blank=False, help_text="Incluindo o número")
    en_bairro = models.CharField(verbose_name="Bairro", max_length=35, blank=False)
    en_cidade = models.CharField(verbose_name="Cidade", max_length=50, blank=False)
    en_estado = BRStateField("Estado")
    en_compl = models.CharField(verbose_name="Complemento", max_length=255,blank=True)
    user = models.ForeignKey(UserCliente, related_name='Usuario', on_delete=models.CASCADE)
    default = models.BooleanField("Padrão", default=False)
    en_criado = models.DateTimeField(auto_now_add=True)
    en_atualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Endereço"
        
    def __str__(self):
        return "Endereço"
    
        