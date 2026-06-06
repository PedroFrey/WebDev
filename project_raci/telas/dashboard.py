from nicegui import ui
from components.layout import pagina
from config import ETAPA_COLORS  # Cores padronizadas para cada etapa
from crud import (
    listar_projetos,
    listar_atividades,
    listar_alocacoes,
    listar_dependencias,
    listar_etapas,
)

def tela_dashboard():
    """
    Tela principal do dashboard que exibe:
    - Cards com métricas gerais (projetos, atividades, alocações, dependências)
    - Distribuição de atividades por etapa
    - Ranking das atividades mais conectadas (com mais dependências)
    """
    
    # ==================== CARREGAMENTO DOS DADOS ====================
    projetos = listar_projetos()
    atividades = listar_atividades()
    alocacoes = listar_alocacoes()
    dependencias = listar_dependencias()
    etapas = listar_etapas()

    # ==================== MÉTRICAS GERAIS ====================
    total_projetos = len(projetos)
    total_atividades = len(atividades)
    total_alocacoes = len(alocacoes)
    total_dependencias = len(dependencias)

    # ==================== DISTRIBUIÇÃO POR ETAPA ====================
    # Inicializa contador zerado para cada etapa
    atividades_por_etapa = {}
    for etapa in etapas:
        atividades_por_etapa[etapa["etapa"]] = 0

    # Conta quantas atividades pertencem a cada etapa
    for atividade in atividades:
        nome_etapa = atividade["etapa"] or "Sem etapa"  # Trata atividades sem etapa
        atividades_por_etapa[nome_etapa] = atividades_por_etapa.get(nome_etapa, 0) + 1

    # ==================== MAPEAMENTO ATIVIDADE -> ETAPA ====================
    # Cria um dicionário para rápido acesso: id_atividade -> nome_da_etapa
    atividade_para_etapa = {}
    for atividade in atividades:
        atividade_para_etapa[atividade["id_atividade"]] = atividade["etapa"] or "Sem etapa"

    # ==================== ANÁLISE DE DEPENDÊNCIAS ====================
    # Identifica quais atividades possuem dependências (como pai ou filho)
    atividades_com_dependencia = set()
    for dep in dependencias:
        atividades_com_dependencia.add(dep["id_atividade_pai"])
        atividades_com_dependencia.add(dep["id_atividade_filho"])

    # Lista de atividades que não possuem nenhuma dependência
    atividades_sem_dependencia = [
        atividade for atividade in atividades
        if atividade["id_atividade"] not in atividades_com_dependencia
    ]

    # ==================== RANKING DE CONEXÕES ====================
    # Conta quantas vezes cada atividade aparece em dependências
    # (quanto maior, mais conectada/importante é a atividade)
    ranking_dependencias = {}
    for dep in dependencias:
        pai = dep["atividade_pai"]
        filho = dep["atividade_filho"]
        ranking_dependencias[pai] = ranking_dependencias.get(pai, 0) + 1
        ranking_dependencias[filho] = ranking_dependencias.get(filho, 0) + 1

    # Ordena do mais conectado para o menos conectado
    ranking_dependencias = sorted(
        ranking_dependencias.items(),
        key=lambda x: x[1],
        reverse=True
    )

    # ==================== CONSTRUÇÃO DA INTERFACE ====================
    with pagina("Dashboard"):
        # Título principal
        ui.label("Visão Geral do Gerenciador").classes("text-3xl font-bold mb-4")

        # ==================== CARDS DE MÉTRICAS ====================
        with ui.row().classes("w-full gap-4"):
            # Card: Projetos
            with ui.card().classes("w-60"):
                ui.label("Projetos").classes("text-lg")
                ui.label(str(total_projetos)).classes("text-4xl font-bold text-blue-700")
            
            # Card: Atividades
            with ui.card().classes("w-60"):
                ui.label("Atividades").classes("text-lg")
                ui.label(str(total_atividades)).classes("text-4xl font-bold text-green-700")
            
            # Card: Alocações RACI
            with ui.card().classes("w-60"):
                ui.label("Alocações RACI").classes("text-lg")
                ui.label(str(total_alocacoes)).classes("text-4xl font-bold text-orange-700")
            
            # Card: Dependências
            with ui.card().classes("w-60"):
                ui.label("Dependências").classes("text-lg")
                ui.label(str(total_dependencias)).classes("text-4xl font-bold text-purple-700")

        # ==================== SEÇÃO INFERIOR (2 COLUNAS) ====================
        with ui.row().classes("w-full mt-6 gap-6"):
            
            # ==================== COLUNA ESQUERDA: ATIVIDADES POR ETAPA ====================
            with ui.card().classes("w-[500px]"):
                ui.label(f"Atividades por Etapa ({str(total_atividades)})").classes("text-xl font-bold")
                
                # Exibe cada etapa com quadradinho colorido e badge com quantidade
                for i, (etapa, qtd) in enumerate(sorted(atividades_por_etapa.items())):
                    # Seleciona a cor baseada no índice, com fallback usando módulo
                    cor = ETAPA_COLORS[i % len(ETAPA_COLORS)] if ETAPA_COLORS else "#64748b"
                    
                    with ui.row().classes("w-full justify-between items-center p-2 rounded"):
                        # Container da etapa (quadradinho colorido + nome)
                        with ui.row().classes("gap-2 items-center"):
                            # Quadradinho colorido representando a etapa
                            ui.element("div").classes(f"w-4 h-4 rounded").style(f"background-color: {cor}")
                            ui.label(etapa).classes("font-medium")
                        
                        # Label com a quantidade, usando a mesma cor da etapa
                        def label_colorido(valor, cor):
                            return ui.label(str(valor)).style(f"""
                                background-color: {cor};
                                color: white;
                                padding: 2px 8px;
                                border-radius: 12px;
                                font-size: 12px;
                                font-weight: bold;
                                min-width: 30px;
                                text-align: center;
                                display: inline-block;
                            """)

                        # Uso:
                        label_colorido(qtd, cor)

            # ==================== COLUNA DIREITA: RANKING DE ATIVIDADES ====================
            with ui.card().classes("w-full"):
                ui.label("Top 10 Atividades Mais Conectadas").classes("text-xl font-bold mb-2")
                ui.label("Atividades com maior número de dependências (como pai ou filho)").classes(
                    "text-sm text-gray-500 mb-4"
                )

                # Prepara os dados para a tabela
                rows = []
                for nome_atividade, qtd in ranking_dependencias[:10]:
                    # Busca a etapa correspondente à atividade
                    id_atividade = None
                    etapa_atividade = "Desconhecida"
                    
                    for a in atividades:
                        if a["atividade"] == nome_atividade:
                            id_atividade = a["id_atividade"]
                            etapa_atividade = atividade_para_etapa.get(id_atividade, "Sem etapa")
                            break
                    
                    rows.append({
                        "etapa": etapa_atividade,
                        "atividade": nome_atividade,
                        "dependencias": qtd,
                    })

                # Tabela com quebra de texto automática e larguras proporcionais
                ui.table(
                    columns=[
                        {"name": "etapa", "label": "Etapa", "field": "etapa", "width": "15%"},
                        {"name": "atividade", "label": "Atividade", "field": "atividade", 
                         "width": "55%", "classes": "whitespace-normal break-words"},
                        {"name": "dependencias", "label": "Dependências", "field": "dependencias", "width": "30%"},
                    ],
                    rows=rows,
                    pagination=10,  # Limita a 10 registros por página
                ).classes("w-full").props("wrap-cells")  # wrap-cells permite quebra de texto