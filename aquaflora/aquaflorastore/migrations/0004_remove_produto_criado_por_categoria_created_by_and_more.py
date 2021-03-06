# Generated by Django 4.0.3 on 2022-05-09 22:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aquaflorastore', '0003_remove_produto_img_2_remove_produto_img_3_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produto',
            name='Criado_por',
        ),
        migrations.AddField(
            model_name='categoria',
            name='created_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='criador_categoria', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='produto',
            name='created_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='criador_produto', to=settings.AUTH_USER_MODEL),
        ),
    ]
