from django.db import models

class Projeto(models.Model):
    nome = models.CharField(max_length=200)

    area = models.CharField(max_length=100)

    responsavel = models.CharField(max_length=100)

    atividade = models.CharField(max_length=200)

    data_inicio = models.DateField()

    duracao_dias = models.IntegerField()

    dependencia = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return self.nome