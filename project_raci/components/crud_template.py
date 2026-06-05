from nicegui import ui


def crud_page(
    titulo: str,
    subtitulo: str,
    columns: list,
    listar_func,
    salvar_func,
    atualizar_func=None,
    excluir_func=None,
    form_builder=None,
    preencher_form=None,
    obter_form=None,
    limpar_form=None,
    key_fields=None,
):

    if key_fields is None:
        key_fields = ["id"]

    registro_em_edicao = {
        "value": None
    }

    dados_originais = []

    ultimo_texto_busca = {
        "value": ""
    }

    def atualizar_tabela():

        nonlocal dados_originais

        dados_originais = [
            dict(r)
            for r in listar_func()
        ]

        aplicar_filtro()

    def aplicar_filtro():

        filtro = busca.value or ""
        filtro = filtro.strip().lower()

        if filtro == "":

            tabela.rows = dados_originais
            tabela.update()
            return

        linhas_filtradas = []

        for row in dados_originais:

            encontrou = False

            for valor in row.values():

                if valor is None:
                    continue

                if filtro in str(valor).lower():
                    encontrou = True
                    break

            if encontrou:
                linhas_filtradas.append(row)

        tabela.rows = linhas_filtradas
        tabela.update()

    def monitorar_busca():

        texto_atual = busca.value or ""

        if texto_atual != ultimo_texto_busca["value"]:

            ultimo_texto_busca["value"] = texto_atual

            aplicar_filtro()

    def salvar():

        dados = obter_form()

        if registro_em_edicao["value"] is None:

            salvar_func(*dados)

            ui.notify(
                "Criado com sucesso",
                color="positive"
            )

        else:

            if atualizar_func:

                atualizar_func(
                    *registro_em_edicao["value"],
                    *dados
                )

                ui.notify(
                    "Atualizado com sucesso",
                    color="positive"
                )

        if limpar_form:
            limpar_form()

        registro_em_edicao["value"] = None

        atualizar_tabela()

    def editar():

        if not preencher_form:
            return

        selecionados = tabela.selected

        if not selecionados:

            ui.notify(
                "Selecione um registro",
                color="warning"
            )

            return

        row = selecionados[0]

        registro_em_edicao["value"] = [
            row[campo]
            for campo in key_fields
        ]

        preencher_form(row)

    def excluir():

        if not excluir_func:
            return

        selecionados = tabela.selected

        if not selecionados:

            ui.notify(
                "Selecione um registro",
                color="warning"
            )

            return

        row = selecionados[0]

        excluir_func(
            *[
                row[campo]
                for campo in key_fields
            ]
        )

        if limpar_form:
            limpar_form()

        atualizar_tabela()

        ui.notify(
            "Excluído com sucesso",
            color="positive"
        )

    with ui.column().classes(
        "w-full items-center bg-slate-100 min-h-screen p-8"
    ):

        ui.label(titulo).classes(
            "text-4xl font-bold text-blue-700"
        )

        ui.label(subtitulo).classes(
            "text-lg text-gray-600 mb-4"
        )

        with ui.card().classes(
            "w-full max-w-5xl shadow-lg"
        ):

            if form_builder:
                form_builder()

            with ui.row().classes(
                "gap-2 mt-4"
            ):

                ui.button(
                    "Salvar",
                    icon="save",
                    on_click=salvar
                ).props("color=primary")

                if atualizar_func:

                    ui.button(
                        "Editar",
                        icon="edit",
                        on_click=editar
                    ).props("color=warning")

                if excluir_func:

                    ui.button(
                        "Excluir",
                        icon="delete",
                        on_click=excluir
                    ).props("color=negative")

                if limpar_form:

                    ui.button(
                        "Cancelar",
                        icon="close",
                        on_click=limpar_form
                    )

        with ui.card().classes(
            "w-full max-w-5xl mt-6 shadow-lg"
        ):

            busca = ui.input(
                label="Buscar em todos os campos"
            ).props(
                "outlined clearable"
            ).classes(
                "w-full mb-4"
            )

            tabela = ui.table(
                columns=columns,
                rows=[],
                row_key=key_fields[0],
                selection="single",
                pagination=10,
            ).classes(
                "w-full"
            )

            ui.timer(
                0.2,
                monitorar_busca
            )

            atualizar_tabela()