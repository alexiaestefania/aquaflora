# Generated by Django 4.0.3 on 2022-05-09 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0007_pedido_statuscancelado_pedido_statusreembolso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='criadoem',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Criado em'),
        ),
    ]
