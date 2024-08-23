from django.db import models

# Create your models here.
class Ativo(models.Model):
    nome = models.CharField(max_length=128)
    codigo = models.CharField(max_length=6)

    def __str__(self):

        return self.codigo

class TunelParametro(models.Model):
    ativo = models.OneToOneField(Ativo, on_delete=models.CASCADE)
    limite_inferior = models.DecimalField(max_digits=10, decimal_places=3)
    limite_superior = models.DecimalField(max_digits=10, decimal_places=3)
    periodicidade = models.IntegerField(help_text="Periodicidade em minutos")
    email = models.EmailField(help_text="Informe seu e-mail para receber alertas")

    def __str__(self):

        return f"Parâmetros de {self.ativo.codigo}"

class Cotacao(models.Model):
    ativo = models.ForeignKey(Ativo, on_delete=models.CASCADE)
    preco_negocio = models.DecimalField(max_digits=10, decimal_places=3)
    #quantidade_negociada = models.IntegerField( help_text="Quantidade de ativos negociados")
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.ativo.codigo} - {self.preco_negocio} às {self.data_hora}"