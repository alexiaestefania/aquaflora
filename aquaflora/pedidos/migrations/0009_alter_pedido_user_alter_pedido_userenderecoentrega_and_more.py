# Generated by Django 4.0.3 on 2022-05-09 22:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conta', '0002_alter_userendereco_en_nomecompleto'),
        ('aquaflora_checkout', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pedidos', '0008_alter_pedido_criadoem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='usuario_pedido', to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='userEnderecoEntrega',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='usuario_endereco', to='conta.userendereco', verbose_name='Endereço de Entrega'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='userFrete',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='opcao_frete', to='aquaflora_checkout.opcoesfrete', verbose_name='Frete Escolhido'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='valorpgto',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=5, verbose_name='Valor Total'),
        ),
    ]
