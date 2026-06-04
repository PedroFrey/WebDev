from db import create_database

from nicegui import ui

from telas.responsaveis import criar_tela

# create_database()
# print("Banco criado com sucesso!")

criar_tela()

ui.run(
    title="Project RACI",
    reload=True
)