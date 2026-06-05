from nicegui import ui

from components.layout import pagina
from components.crud_template import crud_page

from crud import (
    listar_alocacoes,
    listar_projetos,
    listar_legenda_raci,
    listar_areas,
    listar_etapas,
    listar_atividades,
    listar_atividades_por_etapa,
    buscar_atividade,
    criar_alocacao,
    excluir_alocacao,
    atualizar_alocacao,
)


def tela_alocacao():

    projetos = listar_projetos()
    etapas = listar_etapas()
    raci = listar_legenda_raci()
    areas = listar_areas()
    atividades = listar_atividades()

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

    todas_atividades = {
        a["id_atividade"]: a["atividade"]
        for a in atividades
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

                atividade.options = todas_atividades
                atividade.update()

                return

            atividades_filtradas = listar_atividades_por_etapa(
                etapa.value
            )

            atividade.options = {
                a["id_atividade"]: a["atividade"]
                for a in atividades_filtradas
            }

            atividade.value = None
            atividade.update()

        def carregar_etapa():

            if not atividade.value:

                etapa.value = None
                etapa.update()

                return

            dados_atividade = buscar_atividade(
                atividade.value
            )

            if not dados_atividade:
                return

            etapa.value = dados_atividade["id_etapa"]

            atividades_filtradas = listar_atividades_por_etapa(
                dados_atividade["id_etapa"]
            )

            atividade.options = {
                a["id_atividade"]: a["atividade"]
                for a in atividades_filtradas
            }

            atividade.value = dados_atividade["id_atividade"]

            etapa.update()
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
                    on_change=carregar_atividades,
                ).props("outlined").classes("w-48")

                atividade = ui.select(
                    todas_atividades,
                    label="Atividade",
                    on_change=lambda: carregar_etapa(),
                ).props("outlined").classes("w-96")

                atividade.on(
                    "update:model-value",
                    lambda _: carregar_etapa()
                )

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

    def preencher_form(row):

        projeto.value = row["id_projeto"]

        etapa.value = row["id_etapa"]

        atividades_filtradas = listar_atividades_por_etapa(
            row["id_etapa"]
        )

        atividade.options = {
            a["id_atividade"]: a["atividade"]
            for a in atividades_filtradas
        }

        atividade.value = row["id_atividade"]

        raci_sel.value = row["id_raci"]
        area.value = row["id_area"]

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
            "name": "desc_raci",
            "label": "RACI",
            "field": "desc_raci",
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
            atualizar_func=atualizar_alocacao,
            excluir_func=excluir_alocacao,
            preencher_form=preencher_form,
            form_builder=form_builder,
            obter_form=obter_form,
            limpar_form=limpar_form,
            key_fields=[
                "id_projeto",
                "id_atividade",
                "id_raci",
                "id_area",
            ],
        )