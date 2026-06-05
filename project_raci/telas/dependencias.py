from nicegui import ui

from components.layout import pagina

from crud import (
    listar_etapas,
    listar_atividades,
    listar_dependencias,
    listar_dependencias_atividade,
    criar_dependencia,
    excluir_todas_dependencias_atividade,
)

def tela_dependencias():

    etapas = [
        dict(x)
        for x in listar_etapas()
    ]

    atividades = [
        dict(x)
        for x in listar_atividades()
    ]

    etapa_filtro = None
    atividade_focal = None

    predecessoras = []
    sucessoras = []

    painel_predecessoras = ui.column()
    painel_sucessoras = ui.column()
    painel_disponiveis = ui.column()
    painel_resumo = ui.column()

    cores = [
        "#ef4444",
        "#f97316",
        "#eab308",
        "#22c55e",
        "#06b6d4",
        "#3b82f6",
        "#8b5cf6",
        "#ec4899",
        "#14b8a6",
        "#84cc16",
    ]

    cor_etapa = {}

    for i, etapa in enumerate(etapas):
        cor_etapa[
            etapa["id_etapa"]
        ] = cores[i % len(cores)]

    def obter_atividade(id_atividade):

        for atividade in atividades:

            if (
                atividade["id_atividade"]
                == id_atividade
            ):
                return atividade

        return None

    def atualizar_resumo():

        painel_resumo.clear()

        dependencias = [
            dict(x)
            for x in listar_dependencias()
        ]

        ids_classificados = set()

        for dep in dependencias:
            ids_classificados.add(
                dep["id_atividade_pai"]
            )
            ids_classificados.add(
                dep["id_atividade_filho"]
            )

        with painel_resumo:

            ui.label(
                "Resumo Geral"
            ).classes(
                "text-2xl font-bold mb-4"
            )

            with ui.row().classes(
                "w-full gap-8"
            ):

                with ui.card().classes(
                    "w-[650px]"
                ):

                    ui.label(
                        "Dependências Cadastradas"
                    ).classes(
                        "font-bold text-lg"
                    )

                    if not dependencias:
                        ui.label(
                            "Nenhuma dependência cadastrada"
                        )

                    for dep in dependencias:

                        ui.label(
                            f"{dep['atividade_pai']} → {dep['atividade_filho']}"
                        )

                with ui.card().classes(
                    "w-[350px]"
                ):

                    ui.label(
                        "Atividades Sem Dependência"
                    ).classes(
                        "font-bold text-lg"
                    )

                    sem_dependencia = [
                        a
                        for a in atividades
                        if a["id_atividade"]
                        not in ids_classificados
                    ]

                    if not sem_dependencia:
                        ui.label(
                            "Todas classificadas"
                        )

                    for atividade in sem_dependencia:

                        ui.label(
                            atividade["atividade"]
                        )

    def atualizar_telas():

        painel_predecessoras.clear()

        with painel_predecessoras:

            if not predecessoras:

                ui.label(
                    "Nenhuma predecessora"
                )

            for atividade in predecessoras:

                with ui.card().style(
                    f"""
                    background:{cor_etapa.get(atividade['id_etapa'], '#22c55e')};
                    color:white;
                    """
                ).classes(
                    "w-full p-1"
                ):

                    ui.label(
                        atividade["atividade"]
                    ).classes(
                        "font-bold text-sm"
                    )

        painel_sucessoras.clear()

        with painel_sucessoras:

            if not sucessoras:

                ui.label(
                    "Nenhuma sucessora"
                )

            for atividade in sucessoras:

                with ui.card().style(
                    f"""
                    background:{cor_etapa.get(atividade['id_etapa'], '#3b82f6')};
                    color:white;
                    """
                ).classes(
                    "w-full p-1"
                ):

                    ui.label(
                        atividade["atividade"]
                    ).classes(
                        "font-bold text-sm"
                    )

        painel_disponiveis.clear()

        with painel_disponiveis:

            atividades_exibir = atividades

            if etapa_filtro.value:

                atividades_exibir = [
                    a
                    for a in atividades
                    if a["id_etapa"]
                    == etapa_filtro.value
                ]

            with ui.row().classes(
                "w-full gap-2"
            ):

                for atividade in atividades_exibir:

                    if (
                        atividade_focal.value
                        and atividade["id_atividade"]
                        == atividade_focal.value
                    ):
                        continue

                    if any(
                        x["id_atividade"]
                        == atividade["id_atividade"]
                        for x in predecessoras
                    ):
                        continue

                    if any(
                        x["id_atividade"]
                        == atividade["id_atividade"]
                        for x in sucessoras
                    ):
                        continue

                    with ui.card().style(
                        f"""
                        background:
                        {cor_etapa.get(atividade['id_etapa'], '#64748b')};
                        color:white;
                        """
                    ).classes(
                        "w-[260px]"
                    ):

                        ui.label(
                            atividade["atividade"]
                        ).classes(
                            "font-bold text-sm"
                        )

                        ui.label(
                            atividade["etapa"]
                        ).classes(
                            "text-xs"
                        )

                        with ui.row():

                            ui.button(
                                "←",
                                on_click=lambda e, a=atividade:
                                adicionar_predecessora(a)
                            )

                            ui.button(
                                "→",
                                on_click=lambda e, a=atividade:
                                adicionar_sucessora(a)
                            )

        atualizar_resumo()

    def carregar_dependencias():

        predecessoras.clear()
        sucessoras.clear()

        if not atividade_focal.value:

            atualizar_telas()
            return

        deps = listar_dependencias_atividade(
            atividade_focal.value
        )

        for dep in deps:

            dep = dict(dep)

            if (
                dep["id_atividade_filho"]
                == atividade_focal.value
            ):

                atividade = obter_atividade(
                    dep["id_atividade_pai"]
                )

                if atividade:
                    predecessoras.append(
                        atividade
                    )

            elif (
                dep["id_atividade_pai"]
                == atividade_focal.value
            ):

                atividade = obter_atividade(
                    dep["id_atividade_filho"]
                )

                if atividade:
                    sucessoras.append(
                        atividade
                    )

        atualizar_telas()

    def adicionar_predecessora(
        atividade
    ):

        predecessoras.append(
            atividade
        )

        atualizar_telas()

    def adicionar_sucessora(
        atividade
    ):

        sucessoras.append(
            atividade
        )

        atualizar_telas()

    def limpar_etapa():

        etapa_filtro.value = None

        atualizar_telas()

    def salvar():

        if not atividade_focal.value:

            ui.notify(
                "Selecione uma atividade",
                color="negative"
            )

            return

        excluir_todas_dependencias_atividade(
            atividade_focal.value
        )

        for pred in predecessoras:

            criar_dependencia(
                pred["id_atividade"],
                atividade_focal.value
            )

        for suc in sucessoras:

            criar_dependencia(
                atividade_focal.value,
                suc["id_atividade"]
            )

        ui.notify(
            "Dependências salvas",
            color="positive"
        )

        atualizar_resumo()

    def cancelar():

        predecessoras.clear()
        sucessoras.clear()

        atualizar_telas()

    with pagina("Dependências"):

        ui.label(
            "Cadastro de Dependências"
        ).classes(
            "text-3xl font-bold"
        )

        ui.label(
            "Defina predecessoras e sucessoras das atividades"
        )

        with ui.row().classes(
            "w-full gap-4 mt-4"
        ):

            etapa_filtro = ui.select(
                {
                    e["id_etapa"]:
                    e["etapa"]
                    for e in etapas
                },
                label="Filtrar Etapa"
            ).classes(
                "w-72"
            )

            etapa_filtro.on(
                "update:model-value",
                lambda _: atualizar_telas()
            )

            ui.button(
                "Limpar Filtro",
                icon="filter_alt_off",
                on_click=lambda:
                limpar_etapa()
            )

            atividade_focal = ui.select(
                {
                    a["id_atividade"]:
                    a["atividade"]
                    for a in atividades
                },
                label="Atividade Focal"
            ).classes(
                "w-[500px]"
            )

            atividade_focal.on(
                "update:model-value",
                lambda _:
                carregar_dependencias()
            )

        with ui.row().classes(
            "w-full mt-6 justify-center gap-4"
        ):

            with ui.card().classes(
                "w-[280px] min-h-[250px]"
            ):

                ui.label(
                    "PREDECESSORAS"
                ).classes(
                    "font-bold text-lg"
                )

                painel_predecessoras.move(
                    target_container=
                    ui.context.slot.parent
                )

            with ui.card().classes(
                "w-[220px] h-[180px] items-center justify-center"
            ):

                ui.icon(
                    "account_tree"
                ).classes(
                    "text-5xl text-blue-600"
                )

                ui.label(
                    "ATIVIDADE FOCAL"
                ).classes(
                    "font-bold"
                )

            with ui.card().classes(
                "w-[280px] min-h-[250px]"
            ):

                ui.label(
                    "SUCESSORAS"
                ).classes(
                    "font-bold text-lg"
                )

                painel_sucessoras.move(
                    target_container=
                    ui.context.slot.parent
                )

        with ui.card().classes(
            "w-full mt-6"
        ):

            ui.label(
                "Atividades Disponíveis"
            ).classes(
                "text-xl font-bold"
            )

            painel_disponiveis.move(
                target_container=
                ui.context.slot.parent
            )

        with ui.row().classes(
            "gap-4 mt-6"
        ):

            ui.button(
                "Salvar",
                icon="save",
                on_click=salvar
            ).props(
                "color=positive"
            )

            ui.button(
                "Cancelar",
                icon="refresh",
                on_click=cancelar
            ).props(
                "color=negative"
            )

        with ui.card().classes(
            "w-full mt-8"
        ):

            painel_resumo.move(
                target_container=
                ui.context.slot.parent
            )

    atualizar_telas()