from nicegui import ui
from components.layout import pagina
from components.crud_template import crud_page

from crud import (
    listar_areas,
    listar_responsaveis,
    criar_responsavel,
    atualizar_responsavel,
    excluir_responsavel,
)


def tela_responsaveis():
    areas = listar_areas()

    area_options = {
        a["id_area"]: a["area"]
        for a in areas
    }

    nome = None
    area = None

    def form():
        nonlocal nome, area
        with ui.row().classes("w-full gap-4"):

            nome = ui.input("Nome").props("outlined").classes("flex-grow")

            area = ui.select(
            area_options,
            label="Área"
            ).props("outlined").classes("w-32")

    def obter():
        return [
            nome.value.strip(),
            area.value
        ]

    def preencher(row):
        nome.value = row["responsavel"]
        area.value = row["id_area"]

    def limpar():
        nome.value = ""
        area.value = None

    with pagina("Responsáveis"):

        crud_page(
            titulo="Responsáveis",
            subtitulo="Cadastro de pontos focais por áreas",
            columns=[
                {"name": "id_responsavel", "label": "ID", "field": "id_responsavel"},
                {"name": "responsavel", "label": "Responsável", "field": "responsavel"},
                {"name": "area", "label": "Área", "field": "area"},
            ],
            listar_func=listar_responsaveis,
            salvar_func=criar_responsavel,
            atualizar_func=atualizar_responsavel,
            excluir_func=excluir_responsavel,
            form_builder=form,
            obter_form=obter,
            preencher_form=preencher,
            limpar_form=limpar,
            key_fields=["id_responsavel"],
        )