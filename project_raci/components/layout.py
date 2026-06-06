from nicegui import ui

from components.menu import (
    menu_lateral,
    alternar_menu,
)

def pagina(titulo):

    menu_lateral()

    with ui.header().classes(
        'bg-blue-700 text-white'
    ):

        ui.button(
            icon='menu',
            on_click=alternar_menu
        ).props(
            'flat color=white'
        )

        ui.label(
            titulo
        ).classes(
            'text-h5'
        )

    with ui.column().classes(
        'w-full p-6'
    ):
        return ui.column().classes(
            'w-full'
        )