from django.db import models

class OpcoesFrete(models.Model):
    FreteNome = models.CharField(verbose_name='Tipo de Frete', max_length=255, )
    FretePreco = models.DecimalField(verbose_name='Preço do Frete', max_digits=5, decimal_places=2, )
    FreteTempoAprox = models.CharField(verbose_name='Tempo Aproximado', max_length=255, help_text="Recomenda-se que adicione um dia a mais na previsão.")
    Frete_Ativo = models.BooleanField(default=True, help_text="Marque como falso caso queira esconder a opção.")
    
    class Meta:
        verbose_name = 'Opção de Frete'
        verbose_name_plural = 'Opções de Frete'
        
    def __str__(self):
        return self.FreteNome
    