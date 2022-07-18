# Generated by Django 4.0.3 on 2022-04-20 01:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aquaflora_checkout', '0001_initial'),
        ('pedidos', '0002_remove_pedido_usernome'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='userCPF',
        ),
        migrations.AddField(
            model_name='pedido',
            name='userFrete',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='opcao_frete', to='aquaflora_checkout.opcoesfrete', verbose_name='Frete Escolhido'),
            preserve_default=False,
        ),
    ]
