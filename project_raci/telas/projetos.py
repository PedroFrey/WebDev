from nicegui import ui

from components.layout import pagina
from components.crud_template import crud_page

from crud import (
    listar_projetos,
    listar_clientes,
    criar_projeto,
    atualizar_projeto,
    excluir_projeto,
)


def tela_projetos():

    clientes = listar_clientes()

    cliente_options = {
        c["cliente_id"]: c["cliente"]
        for c in clientes
    }

    nome = None
    cliente = None

    def form_builder():
        nonlocal nome, cliente

        with ui.row().classes("w-full gap-4 items-end"):

            nome = ui.input("Nome do Projeto") \
                .props("outlined") \
                .classes("flex-grow")

            cliente = ui.select(
                cliente_options,
                label="Cliente",
            ).props("outlined").classes("w-64")

    def obter_form():
        return [
            cliente.value,
            nome.value.strip(),
        ]

    def preencher_form(row):
        nome.value = row["projeto"]

        # precisa converter cliente nome → id
        for c in clientes:
            if c["cliente"] == row["cliente"]:
                cliente.value = c["cliente_id"]
                break

    def limpar_form():
        nome.value = ""
        cliente.value = None

    columns = [
        {
            "name": "id_projeto",
            "label": "ID",
            "field": "id_projeto",
            "align": "left",
        },
        {
            "name": "projeto",
            "label": "Projeto",
            "field": "projeto",
            "align": "left",
        },
        {
            "name": "cliente",
            "label": "Cliente",
            "field": "cliente",
            "align": "left",
        },
    ]

    with pagina("Projetos"):

        crud_page(
            titulo="Projetos",
            subtitulo="Cadastro de projetos",
            columns=columns,
            listar_func=listar_projetos,
            salvar_func=criar_projeto,
            atualizar_func=atualizar_projeto,
            excluir_func=excluir_projeto,
            form_builder=form_builder,
            obter_form=obter_form,
            preencher_form=preencher_form,
            limpar_form=limpar_form,
            id_field="id_projeto",
        )