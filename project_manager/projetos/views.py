from django.shortcuts import render, redirect
from .models import Projeto


def home(request):

    if request.method == "POST":

        Projeto.objects.create(
            nome=request.POST["nome"],
            area=request.POST["area"],
            responsavel=request.POST["responsavel"],
            atividade=request.POST["atividade"],
            data_inicio=request.POST["data_inicio"],
            duracao_dias=request.POST["duracao_dias"],
            dependencia=request.POST["dependencia"],
        )

        return redirect("/")

    projetos = Projeto.objects.all()

    return render(
        request,
        "home.html",
        {
            "projetos": projetos
        }
    )