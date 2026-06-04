from nicegui import ui

from crud import (
    listar_areas,
    criar_responsavel,
    listar_responsaveis
)


def criar_tela():

    areas = listar_areas()

    area_options = {
        area["id_area"]: area["area"]
        for area in areas
    }

    nome = ui.input("Responsável")

    area = ui.select(
        options=area_options,
        label="Área"
    )

    tabela = ui.table(
        columns=[
            {
                "name": "id",
                "label": "ID",
                "field": "id_responsavel"
            },
            {
                "name": "responsavel",
                "label": "Responsável",
                "field": "responsavel"
            },
            {
                "name": "area",
                "label": "Área",
                "field": "area"
            },
        ],
        rows=[],
        row_key="id_responsavel"
    )


    def atualizar_tabela():
        tabela.rows = [
            dict(row)
            for row in listar_responsaveis()
        ]
        tabela.update()


    def salvar():
        criar_responsavel(
            nome.value,
            area.value
        )

        nome.value = ""

        atualizar_tabela()


    ui.button(
        "Salvar",
        on_click=salvar
    )

    atualizar_tabela()