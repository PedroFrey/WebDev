from nicegui import ui


def menu_lateral():

    with ui.left_drawer().classes(
        'bg-slate-800 text-white'
    ):

        ui.label(
            'PROJETO RACI'
        ).classes(
            'text-h6 q-pa-md'
        )

        ui.separator()

        ui.button(
            'Dashboard',
            icon='dashboard',
            on_click=lambda: ui.navigate.to('/')
        ).props('flat color=white')

        ui.button(
            'Responsáveis',
            icon='people',
            on_click=lambda: ui.navigate.to('/responsaveis')
        ).props('flat color=white')

        ui.button(
            'Projetos',
            icon='folder',
            on_click=lambda: ui.navigate.to('/projetos')
        ).props('flat color=white')

        ui.button(
            'Atividades',
            icon='task',
            on_click=lambda: ui.navigate.to('/atividades')
        ).props('flat color=white')

        ui.button(
            'Dependências',
            icon='account_tree',
            on_click=lambda: ui.navigate.to('/dependencias')
        ).props('flat color=white')

        ui.button(
            'Gantt',
            icon='timeline',
            on_click=lambda: ui.navigate.to('/gantt')
        ).props('flat color=white')