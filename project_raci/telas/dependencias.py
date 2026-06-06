from nicegui import ui
from components.layout import pagina
from config import ETAPA_COLORS
from crud import (
    listar_etapas,
    listar_atividades,
    listar_dependencias,
    listar_dependencias_atividade,
    criar_dependencia,
    excluir_todas_dependencias_atividade,
)

# Mapeamento de etapas para letras
ETAPAS_LETRAS = {
    "Deep Dive": "A",
    "Governança": "B", 
    "Set-up": "C",
    "Warm-up": "D",
    "Go-live": "E",
    "Manutenção": "F"
}

def tela_dependencias():

    etapas = [dict(x) for x in listar_etapas()]
    atividades = [dict(x) for x in listar_atividades()]

    etapa_filtro = None
    atividade_focal = None
    predecessoras = []
    sucessoras = []

    painel_predecessoras = ui.column()
    painel_sucessoras = ui.column()
    painel_disponiveis = ui.column()
    painel_resumo = ui.column()

    # Mapeia cores para cada etapa
    cor_etapa = {}
    for i, etapa in enumerate(etapas):
        cor_etapa[etapa["id_etapa"]] = ETAPA_COLORS[i % len(ETAPA_COLORS)] if ETAPA_COLORS else "#64748b"

    def obter_atividade(id_atividade):
        for atividade in atividades:
            if atividade["id_atividade"] == id_atividade:
                return atividade
        return None

    def atualizar_resumo():
        """Atualiza o painel de resumo com visual de escada/waterfall"""
        painel_resumo.clear()
        
        dependencias = [dict(x) for x in listar_dependencias()]
        
        # Agrupa dependências por etapa
        dependencias_por_etapa = {etapa["etapa"]: [] for etapa in etapas}
        
        for dep in dependencias:
            # Encontra a etapa da atividade pai
            etapa_pai = "Sem etapa"
            for a in atividades:
                if a["atividade"] == dep["atividade_pai"]:
                    etapa_pai = a["etapa"] or "Sem etapa"
                    break
            dependencias_por_etapa[etapa_pai].append(dep)
        
        # Identifica atividades sem dependência
        ids_classificados = set()
        for dep in dependencias:
            ids_classificados.add(dep["id_atividade_pai"])
            ids_classificados.add(dep["id_atividade_filho"])
        
        sem_dependencia = [
            a for a in atividades
            if a["id_atividade"] not in ids_classificados
        ]
        
        with painel_resumo:
            # Título
            with ui.row().classes("items-center gap-2 mb-4"):
                ui.icon("waterfall_chart", size="28px").classes("text-primary")
                ui.label("Waterfall de Dependências").classes("text-2xl font-bold")
                ui.badge("Visualização em Escada", color="primary")
            
            # Mapa/Waterfall visual
            with ui.card().classes("w-full shadow-lg mb-6 overflow-x-auto"):
                ui.label("📊 Sequência de Dependências por Etapa").classes("font-bold text-lg mb-3")
                
                # Cabeçalho com as letras das etapas
                with ui.row().classes("gap-0 mb-2 border-b-2 border-gray-200"):
                    etapas_ordenadas = ["Deep Dive", "Governança", "Set-up", "Warm-up", "Go-live", "Manutenção"]
                    for etapa in etapas_ordenadas:
                        if etapa in ETAPAS_LETRAS:
                            with ui.column().classes("flex-1 text-center p-2"):
                                cor = cor_etapa.get([e["id_etapa"] for e in etapas if e["etapa"] == etapa][0] if any(e["etapa"] == etapa for e in etapas) else 0, "#64748b")
                                ui.element("div").classes("w-8 h-8 rounded-full mx-auto").style(f"background-color: {cor}; line-height: 32px; text-align: center; color: white; font-weight: bold; font-size: 18px")
                                ui.label(ETAPAS_LETRAS[etapa]).classes("font-bold mt-1")
                                ui.label(etapa).classes("text-xs text-gray-500")
                
                # Linhas de conexão estilo waterfall
                with ui.column().classes("gap-3 mt-4"):
                    for i, etapa in enumerate(etapas_ordenadas):
                        if dependencias_por_etapa.get(etapa):
                            cor = cor_etapa.get([e["id_etapa"] for e in etapas if e["etapa"] == etapa][0] if any(e["etapa"] == etapa for e in etapas) else 0, "#64748b")
                            
                            with ui.row().classes("items-start gap-2 p-2 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800"):
                                # Indicador de etapa
                                with ui.column().classes("items-center w-16"):
                                    ui.element("div").classes("w-10 h-10 rounded-full").style(f"background-color: {cor}; line-height: 40px; text-align: center; color: white; font-weight: bold; font-size: 20px")
                                    ui.label(ETAPAS_LETRAS[etapa]).classes("font-bold")
                                    ui.label(etapa.split("-")[0]).classes("text-xs text-gray-500")
                                
                                # Setas e dependências
                                with ui.column().classes("flex-1 gap-2"):
                                    for dep in dependencias_por_etapa[etapa]:
                                        # Encontra a etapa da atividade filho
                                        etapa_filho = "Sem etapa"
                                        for a in atividades:
                                            if a["atividade"] == dep["atividade_filho"]:
                                                etapa_filho = a["etapa"] or "Sem etapa"
                                                break
                                        
                                        letra_filho = ETAPAS_LETRAS.get(etapa_filho, "?")
                                        
                                        with ui.row().classes("items-center gap-2 p-2 rounded border-l-4").style(f"border-left-color: {cor}"):
                                            ui.chip(dep["atividade_pai"][:30]).style(f"background-color: {cor}; color: white;")
                                            ui.icon("arrow_forward", size="20px").classes("text-gray-500")
                                            ui.chip(dep["atividade_filho"][:30]).style(f"background-color: {cor_etapa.get([e['id_etapa'] for e in etapas if e['etapa'] == etapa_filho][0] if any(e['etapa'] == etapa_filho for e in etapas) else 0, '#64748b')}; color: white;")
                                            ui.badge(letra_filho, color="grey").props("outline")
                        
                        elif i < len(etapas_ordenadas) - 1:
                            # Linha de conexão visual
                            with ui.row().classes("justify-center py-1"):
                                ui.icon("arrow_downward", size="24px").classes("text-gray-300")
            
            # Atividades Sem Dependência em grid visual
            with ui.card().classes("w-full shadow-lg"):
                with ui.row().classes("items-center gap-2 mb-3 flex-wrap"):
                    ui.icon("checklist", size="20px").classes("text-green-600")
                    ui.label("Atividades Sem Dependência").classes("font-bold text-lg")
                    ui.badge(str(len(sem_dependencia)), color="green")
                
                if not sem_dependencia:
                    with ui.column().classes("items-center justify-center p-8 gap-2"):
                        ui.icon("check_circle", size="48px").classes("text-green-500")
                        ui.label("Todas as atividades estão conectadas!").classes("text-green-600 font-medium")
                else:
                    # Grid de cards coloridos
                    with ui.row().classes("gap-3 max-h-96 overflow-auto flex-wrap"):
                        for atividade in sem_dependencia[:20]:
                            cor = cor_etapa.get(atividade["id_etapa"], "#64748b")
                            letra = ETAPAS_LETRAS.get(atividade["etapa"], "?")
                            with ui.card().style(f"background: {cor}10; border-left: 4px solid {cor}").classes("w-[280px] hover:shadow-md transition-shadow"):
                                with ui.row().classes("items-start justify-between gap-2"):
                                    with ui.column().classes("flex-1"):
                                        ui.label(atividade["atividade"]).classes("font-bold text-sm")
                                        with ui.row().classes("items-center gap-1 mt-1"):
                                            ui.element("div").classes("w-3 h-3 rounded-full").style(f"background-color: {cor}")
                                            ui.label(f"Etapa {letra}: {atividade['etapa']}").classes("text-xs text-gray-500")
                                    ui.badge(letra, color="grey").style(f"background-color: {cor}; color: white;")
                        
                        if len(sem_dependencia) > 20:
                            with ui.card().classes("items-center justify-center w-[280px] h-[100px] bg-gray-100 dark:bg-gray-800"):
                                ui.label(f"+{len(sem_dependencia) - 20}").classes("text-2xl font-bold text-gray-500")
                                ui.label("mais atividades").classes("text-xs text-gray-500")

    def atualizar_telas():
        """Atualiza os painéis de predecessoras, sucessoras e disponíveis"""
        painel_predecessoras.clear()
        
        with painel_predecessoras:
            if not predecessoras:
                with ui.column().classes("items-center justify-center p-4 gap-2"):
                    ui.icon("arrow_back", size="32px").classes("text-gray-400")
                    ui.label("Nenhuma predecessora").classes("text-gray-500 text-sm")
            else:
                for atividade in predecessoras:
                    cor = cor_etapa.get(atividade['id_etapa'], '#22c55e')
                    letra = ETAPAS_LETRAS.get(atividade['etapa'], "?")
                    with ui.card().style(f"background: {cor}; color: white;").classes("w-full p-2 cursor-pointer hover:opacity-90"):
                        with ui.row().classes("items-center gap-2"):
                            ui.badge(letra).style(f"background: white; color: {cor};")
                            ui.label(atividade["atividade"]).classes("font-bold text-sm")
                        ui.label(atividade["etapa"]).classes("text-xs opacity-80")
        
        painel_sucessoras.clear()
        with painel_sucessoras:
            if not sucessoras:
                with ui.column().classes("items-center justify-center p-4 gap-2"):
                    ui.icon("arrow_forward", size="32px").classes("text-gray-400")
                    ui.label("Nenhuma sucessora").classes("text-gray-500 text-sm")
            else:
                for atividade in sucessoras:
                    cor = cor_etapa.get(atividade['id_etapa'], '#3b82f6')
                    letra = ETAPAS_LETRAS.get(atividade['etapa'], "?")
                    with ui.card().style(f"background: {cor}; color: white;").classes("w-full p-2 cursor-pointer hover:opacity-90"):
                        with ui.row().classes("items-center gap-2"):
                            ui.label(atividade["atividade"]).classes("font-bold text-sm")
                            ui.badge(letra).style(f"background: white; color: {cor};")
                        ui.label(atividade["etapa"]).classes("text-xs opacity-80")
        
        painel_disponiveis.clear()
        with painel_disponiveis:
            atividades_exibir = atividades
            if etapa_filtro and etapa_filtro.value:
                atividades_exibir = [a for a in atividades if a["id_etapa"] == etapa_filtro.value]
            
            if not atividades_exibir:
                with ui.column().classes("items-center justify-center p-8"):
                    ui.label("Nenhuma atividade disponível").classes("text-gray-500")
            else:
                # Agrupa atividades por etapa para visualização em escada
                atividades_por_etapa = {}
                for a in atividades_exibir:
                    etapa_nome = a["etapa"] or "Sem etapa"
                    if etapa_nome not in atividades_por_etapa:
                        atividades_por_etapa[etapa_nome] = []
                    atividades_por_etapa[etapa_nome].append(a)
                
                # Ordem correta das etapas
                ordem_etapas = ["Deep Dive", "Governança", "Set-up", "Warm-up", "Go-live", "Manutenção", "Sem etapa"]
                
                with ui.column().classes("w-full gap-4"):
                    for etapa_nome in ordem_etapas:
                        if etapa_nome in atividades_por_etapa:
                            cor = cor_etapa.get([e["id_etapa"] for e in etapas if e["etapa"] == etapa_nome][0] if any(e["etapa"] == etapa_nome for e in etapas) else 0, "#64748b") if etapa_nome != "Sem etapa" else "#64748b"
                            letra = ETAPAS_LETRAS.get(etapa_nome, "?") if etapa_nome != "Sem etapa" else "?"
                            
                            with ui.row().classes("items-start gap-3 w-full"):
                                # Coluna da etapa
                                with ui.column().classes("items-center w-24 pt-2"):
                                    ui.element("div").classes("w-10 h-10 rounded-full").style(f"background-color: {cor}; line-height: 40px; text-align: center; color: white; font-weight: bold; font-size: 18px")
                                    ui.label(letra).classes("font-bold text-sm")
                                    ui.label(etapa_nome.split("-")[0] if etapa_nome != "Sem etapa" else "Sem").classes("text-xs text-gray-500")
                                
                                # Cards das atividades
                                with ui.row().classes("gap-2 flex-1 flex-wrap"):
                                    for atividade in atividades_por_etapa[etapa_nome]:
                                        if (atividade_focal and atividade_focal.value and atividade["id_atividade"] == atividade_focal.value):
                                            continue
                                        if any(x["id_atividade"] == atividade["id_atividade"] for x in predecessoras):
                                            continue
                                        if any(x["id_atividade"] == atividade["id_atividade"] for x in sucessoras):
                                            continue
                                        
                                        with ui.card().style(f"background: {cor}; color: white;").classes("w-[240px] hover:scale-105 transition-transform"):
                                            ui.label(atividade["atividade"]).classes("font-bold text-sm")
                                            ui.label(atividade["etapa"]).classes("text-xs opacity-80")
                                            with ui.row().classes("gap-2 mt-2 justify-end"):
                                                ui.button("←", on_click=lambda e, a=atividade: adicionar_predecessora(a)).props("dense flat size=sm").classes("text-white")
                                                ui.button("→", on_click=lambda e, a=atividade: adicionar_sucessora(a)).props("dense flat size=sm").classes("text-white")
                    
                    if etapa_filtro and not etapa_filtro.value:
                        ui.separator()
                        ui.label("💡 Dica: Clique nos botões ← e → para adicionar dependências").classes("text-xs text-gray-500 text-center py-2")

        atualizar_resumo()

    # Funções de manipulação (mantidas iguais)
    def carregar_dependencias():
        predecessoras.clear()
        sucessoras.clear()
        if not atividade_focal.value:
            atualizar_telas()
            return
        deps = listar_dependencias_atividade(atividade_focal.value)
        for dep in deps:
            dep = dict(dep)
            if dep["id_atividade_filho"] == atividade_focal.value:
                atividade = obter_atividade(dep["id_atividade_pai"])
                if atividade:
                    predecessoras.append(atividade)
            elif dep["id_atividade_pai"] == atividade_focal.value:
                atividade = obter_atividade(dep["id_atividade_filho"])
                if atividade:
                    sucessoras.append(atividade)
        atualizar_telas()

    def adicionar_predecessora(atividade):
        predecessoras.append(atividade)
        atualizar_telas()

    def adicionar_sucessora(atividade):
        sucessoras.append(atividade)
        atualizar_telas()

    def limpar_etapa():
        etapa_filtro.value = None
        atualizar_telas()

    def salvar():
        if not atividade_focal.value:
            ui.notify("Selecione uma atividade", color="negative")
            return
        excluir_todas_dependencias_atividade(atividade_focal.value)
        for pred in predecessoras:
            criar_dependencia(pred["id_atividade"], atividade_focal.value)
        for suc in sucessoras:
            criar_dependencia(atividade_focal.value, suc["id_atividade"])
        ui.notify("Dependências salvas!", color="positive", position="top")
        atualizar_resumo()

    def cancelar():
        predecessoras.clear()
        sucessoras.clear()
        atualizar_telas()

    # UI Principal
    with pagina("Dependências"):
        ui.label("🏗️ Escada de Dependências (Waterfall)").classes("text-3xl font-bold")
        ui.label("Defina predecessoras (←) e sucessoras (→) organizadas por etapas").classes("text-gray-500 mb-4")
        
        # Legendas das letras
        with ui.row().classes("gap-2 mb-4 flex-wrap justify-center"):
            for etapa in ["Deep Dive", "Governança", "Set-up", "Warm-up", "Go-live", "Manutenção"]:
                if etapa in ETAPAS_LETRAS:
                    cor = cor_etapa.get([e["id_etapa"] for e in etapas if e["etapa"] == etapa][0] if any(e["etapa"] == etapa for e in etapas) else 0, "#64748b")
                    ui.chip(f"{ETAPAS_LETRAS[etapa]} = {etapa}").style(f"background-color: #000000 !important; color: {cor}; border: 1px solid {cor}")
        with ui.row().classes("w-full gap-4 mt-4 flex-wrap"):
            etapa_filtro = ui.select(
                {e["id_etapa"]: e["etapa"] for e in etapas},
                label="Filtrar Etapa"
            ).classes("w-72")
            etapa_filtro.on("update:model-value", lambda _: atualizar_telas())
            
            ui.button("Limpar Filtro", icon="filter_alt_off", on_click=lambda: limpar_etapa()).props("flat")
            
            atividade_focal = ui.select(
                {a["id_atividade"]: a["atividade"] for a in atividades},
                label="Atividade Focal"
            ).classes("flex-grow")
            atividade_focal.on("update:model-value", lambda _: carregar_dependencias())
        
        # Layout principal com cards
        with ui.row().classes("w-full mt-6 justify-center gap-4 flex-wrap"):
            with ui.card().classes("w-[280px] min-h-[300px]"):
                ui.label("⬅️ PREDECESSORAS").classes("font-bold text-lg text-center")
                ui.separator()
                painel_predecessoras.move(target_container=ui.context.slot.parent)
            
            with ui.card().classes("w-[220px] items-center justify-center").style("min-height: 300px"):
                ui.icon("account_tree", size="48px").classes("text-primary")
                ui.label("🎯 ATIVIDADE FOCAL").classes("font-bold text-center mt-2")
                if atividade_focal.value:
                    # Mostra a letra da etapa da atividade focal
                    for a in atividades:
                        if a["id_atividade"] == atividade_focal.value:
                            letra = ETAPAS_LETRAS.get(a["etapa"], "?")
                            ui.chip(f"Etapa {letra}").classes("mt-2")
                            break
            
            with ui.card().classes("w-[280px] min-h-[300px]"):
                ui.label("SUCESSORAS ➡️").classes("font-bold text-lg text-center")
                ui.separator()
                painel_sucessoras.move(target_container=ui.context.slot.parent)
        
        with ui.card().classes("w-full mt-6"):
            ui.label("📋 Atividades Disponíveis (organizadas por etapa)").classes("text-xl font-bold mb-2")
            ui.separator()
            painel_disponiveis.move(target_container=ui.context.slot.parent)
        
        with ui.row().classes("gap-4 mt-6 justify-center"):
            ui.button("💾 Salvar", icon="save", on_click=salvar).props("color=positive")
            ui.button("🔄 Cancelar", icon="refresh", on_click=cancelar).props("color=negative")
        
        with ui.card().classes("w-full mt-8"):
            painel_resumo.move(target_container=ui.context.slot.parent)
    
    atualizar_telas()