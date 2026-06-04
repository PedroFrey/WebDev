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
    id_field="id",
):

    id_em_edicao = {"value": None}

    def atualizar_tabela():
        tabela.rows = [dict(r) for r in listar_func()]
        tabela.update()

    def salvar():
        dados = obter_form()

        if id_em_edicao["value"] is None:
            salvar_func(*dados)
            ui.notify("Criado com sucesso", color="positive")
        else:
            atualizar_func(id_em_edicao["value"], *dados)
            ui.notify("Atualizado com sucesso", color="positive")

        limpar_form()
        id_em_edicao["value"] = None
        atualizar_tabela()

    def editar():
        sel = tabela.selected
        if not sel:
            ui.notify("Selecione um registro", color="warning")
            return

        row = sel[0]
        id_em_edicao["value"] = row[id_field]

        preencher_form(row)

    def excluir():
        sel = tabela.selected
        if not sel:
            ui.notify("Selecione um registro", color="warning")
            return

        row = sel[0]
        excluir_func(row[id_field])

        limpar_form()
        atualizar_tabela()

        ui.notify("Excluído", color="positive")

    with ui.column().classes("w-full items-center bg-slate-100 min-h-screen p-8"):

        ui.label(titulo).classes("text-4xl font-bold text-blue-700")
        ui.label(subtitulo).classes("text-lg text-gray-600 mb-4")

        with ui.card().classes("w-full max-w-5xl shadow-lg"):

            form_builder()

            with ui.row().classes("gap-2 mt-4"):

                ui.button("Salvar", icon="save", on_click=salvar)
                ui.button("Editar", icon="edit", on_click=editar).props("color=warning")
                ui.button("Excluir", icon="delete", on_click=excluir).props("color=negative")
                ui.button("Cancelar", icon="close", on_click=limpar_form)

        with ui.card().classes("w-full max-w-5xl mt-6 shadow-lg"):

            tabela = ui.table(
                columns=columns,
                rows=[],
                row_key=id_field,
                selection="single",
                pagination=10,
            ).classes("w-full")

            atualizar_tabela()