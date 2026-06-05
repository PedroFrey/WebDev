from nicegui import ui

from db import create_database

from telas.dashboard import tela_dashboard
from telas.responsaveis import tela_responsaveis
from telas.projetos import tela_projetos
from telas.alocacoes import tela_alocacao
from telas.dependencias import tela_dependencias
from telas.gantt import tela_gantt

create_database()


@ui.page('/')
def dashboard():
    tela_dashboard()


@ui.page('/responsaveis')
def responsaveis():
    tela_responsaveis()


@ui.page('/projetos')
def projetos():
    tela_projetos()


@ui.page('/alocacoes')
def atividades():
    tela_alocacao()


@ui.page('/dependencias')
def dependencias():
    tela_dependencias()


@ui.page('/gantt')
def gantt():
    tela_gantt()


ui.run(
    title='Projeto RACI',
    reload=True
)