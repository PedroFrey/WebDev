from nicegui import ui

from components.layout import pagina
from components.crud_template import crud_page

from crud import (
    listar_alocacoes,
    listar_projetos,
    listar_legenda_raci,
    listar_areas,
    listar_etapas,
    listar_atividades_por_etapa,
    criar_alocacao,
)


def tela_alocacao():

    projetos = listar_projetos()
    etapas = listar_etapas()
    raci = listar_legenda_raci()
    areas = listar_areas()

    projeto_opt = {
        p["id_projeto"]: p["projeto"]
        for p in projetos
    }

    etapa_opt = {
        e["id_etapa"]: e["etapa"]
        for e in etapas
    }

    raci_opt = {
        r["id_raci"]: r["desc_raci"]
        for r in raci
    }

    area_opt = {
        a["id_area"]: a["area"]
        for a in areas
    }

    projeto = None
    etapa = None
    atividade = None
    raci_sel = None
    area = None

    def form_builder():

        nonlocal projeto
        nonlocal etapa
        nonlocal atividade
        nonlocal raci_sel
        nonlocal area

        def carregar_atividades():

            if not etapa.value:
                atividade.options = {}
                atividade.value = None
                atividade.update()
                return

            atividades = listar_atividades_por_etapa(
                etapa.value
            )

            atividade.options = {
                a["id_atividade"]: a["atividade"]
                for a in atividades
            }

            atividade.value = None
            atividade.update()

        with ui.column().classes("w-full gap-4"):

            with ui.row().classes("w-full gap-4"):

                projeto = ui.select(
                    projeto_opt,
                    label="Projeto"
                ).props("outlined").classes("w-72")

                etapa = ui.select(
                    etapa_opt,
                    label="Etapa",
                    on_change=carregar_atividades
                ).props("outlined").classes("w-36")

                atividade = ui.select(
                    {},
                    label="Atividade"
                ).props("outlined").classes("w-96")

            with ui.row().classes("w-full gap-4"):

                area = ui.select(
                    area_opt,
                    label="Área"
                ).props("outlined").classes("w-72")

                raci_sel = ui.select(
                    raci_opt,
                    label="RACI"
                ).props("outlined").classes("w-48")



    def obter_form():

        return [
            projeto.value,
            atividade.value,
            raci_sel.value,
            area.value,
        ]

    def limpar_form():

        for campo in [
            projeto,
            etapa,
            atividade,
            raci_sel,
            area,
        ]:
            if campo:
                campo.value = None

    columns = [
        {
            "name": "projeto",
            "label": "Projeto",
            "field": "projeto",
        },
        {
            "name": "atividade",
            "label": "Atividade",
            "field": "atividade",
        },
        {
            "name": "legenda_raci",
            "label": "RACI",
            "field": "legenda_raci",
        },
        {
            "name": "area",
            "label": "Área",
            "field": "area",
        },
    ]

    with pagina("Alocação"):

        crud_page(
            titulo="Alocação",
            subtitulo="RACI de projetos e atividades",
            columns=columns,
            listar_func=listar_alocacoes,
            salvar_func=criar_alocacao,
            form_builder=form_builder,
            obter_form=obter_form,
            limpar_form=limpar_form,
            id_field=None,
        )