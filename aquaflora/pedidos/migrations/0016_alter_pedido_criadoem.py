# Generated by Django 4.0.5 on 2022-06-13 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0015_alter_itempedido_preco_alter_pedido_valorpgto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='criadoem',
            field=models.DateField(auto_now_add=True, verbose_name='Criado em'),
        ),
    ]