from django.db import models

class Area(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Responsavel(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.nome


class Projeto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome


class Etapa(models.Model):
    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE
    )

    nome = models.CharField(max_length=200)

    data_inicio = models.DateField()
    data_fim = models.DateField()

    responsavel = models.ForeignKey(
        Responsavel,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.nome