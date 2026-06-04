from nicegui import ui
from components.menu import menu_lateral


def pagina(titulo):

    menu_lateral()

    with ui.header().classes(
        'bg-blue-700 text-white'
    ):
        ui.label(titulo).classes(
            'text-h5'
        )

    with ui.column().classes(
        'w-full p-6'
    ):
        return ui.column().classes(
            'w-full'
        )