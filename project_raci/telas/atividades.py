from nicegui import ui

from components.layout import pagina
from components.crud_template import crud_page

from crud import (
    listar_alocacoes,
    listar_projetos,
    listar_atividades,
    listar_responsaveis,
    listar_legenda_raci,
    listar_areas,
    criar_alocacao,
)


def tela_alocacao():

    projetos = listar_projetos()
    atividades = listar_atividades()
    responsaveis = listar_responsaveis()
    raci = listar_legenda_raci()
    areas = listar_areas()

    projeto_opt = {p["id_projeto"]: p["projeto"] for p in projetos}
    atividade_opt = {a["id_atividade"]: a["atividade"] for a in atividades}
    resp_opt = {r["id_responsavel"]: r["responsavel"] for r in responsaveis}
    raci_opt = {r["id_raci"]: r["legenda_raci"] for r in raci}
    area_opt = {a["id_area"]: a["area"] for a in areas}

    projeto = atividade = responsavel = raci_sel = area = None
    dt_ini = dt_fim = None

    def form_builder():

        nonlocal projeto, atividade, responsavel, raci_sel, area, dt_ini, dt_fim

        with ui.column().classes("w-full gap-4"):

            with ui.row().classes("w-full gap-4"):

                projeto = ui.select(projeto_opt, label="Projeto").classes("w-64")
                atividade = ui.select(atividade_opt, label="Atividade").classes("w-64")
                responsavel = ui.select(resp_opt, label="Responsável").classes("w-64")

            with ui.row().classes("w-full gap-4"):

                raci_sel = ui.select(raci_opt, label="RACI").classes("w-64")
                area = ui.select(area_opt, label="Área").classes("w-64")


    def obter_form():
        return [
            projeto.value,
            atividade.value,
            responsavel.value,
            raci_sel.value,
            area.value,
        ]

    def limpar_form():
        for v in [projeto, atividade, responsavel, raci_sel, area]:
            v.value = None

    columns = [
        {"name": "projeto", "label": "Projeto", "field": "projeto"},
        {"name": "atividade", "label": "Atividade", "field": "atividade"},
        {"name": "responsavel", "label": "Responsável", "field": "responsavel"},
        {"name": "legenda_raci", "label": "RACI", "field": "legenda_raci"},
        {"name": "area", "label": "Área", "field": "area"},
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
            id_field=None  # ainda não vamos editar/excluir aqui
        )