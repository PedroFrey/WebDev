from nicegui import ui
from db import create_database
from telas.dashboard import tela_dashboard
from telas.responsaveis import tela_responsaveis
from telas.projetos import tela_projetos
from telas.alocacoes import tela_alocacao
from telas.dependencias import tela_dependencias
from telas.gantt import tela_gantt

# Configurações
APP_CONFIG = {
    "title": "Projeto RACI - Gerenciamento de Matriz de Responsabilidades",
    "favicon": "📊",
    "dark_mode": True,
    "storage_secret": "your-secret-key-here",  # Mude para uma chave segura em produção
}

def init_app():
    """Inicializa a aplicação"""
    try:
        create_database()
        print("✅ Banco de dados inicializado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao inicializar banco de dados: {e}")
        raise

# Inicializa
init_app()

# Rotas
@ui.page('/')
def dashboard():
    tela_dashboard()

@ui.page('/responsaveis')
def responsaveis():
    tela_responsaveis()

@ui.page('/projetos')
def projetos():
    tela_projetos()

@ui.page('/alocacoes')
def atividades():
    tela_alocacao()

@ui.page('/dependencias')
def dependencias():
    tela_dependencias()

@ui.page('/gantt')
def gantt():
    tela_gantt()

# Configuração da aplicação
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title=APP_CONFIG["title"],
        favicon=APP_CONFIG["favicon"],
        dark=APP_CONFIG["dark_mode"],
        host='0.0.0.0',
        port=8080,
        reload=False
    )