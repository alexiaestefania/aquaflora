# Generated by Django 4.0.3 on 2022-04-19 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='userNome',
        ),
    ]