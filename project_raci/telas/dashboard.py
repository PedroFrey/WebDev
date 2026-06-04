from nicegui import ui
from components.layout import pagina


def tela_dashboard():

    with pagina('Dashboard'):

        ui.label(
            'Bem-vindo ao Projeto RACI'
        ).classes(
            'text-h4'
        )