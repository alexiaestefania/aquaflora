# Generated by Django 4.0.5 on 2022-06-25 22:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aquaflorastore', '0011_remove_produto_livro_qtdd_alter_categoria_cat_ativa_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='produto',
            options={'ordering': ('-livro_criadoem',), 'verbose_name': 'Livro'},
        ),
    ]
