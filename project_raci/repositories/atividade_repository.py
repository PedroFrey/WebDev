from db import get_connection


def listar_atividades_por_etapa(id_etapa):

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            id_atividade,
            atividade
        FROM tb_atividade
        WHERE id_etapa = ?
        ORDER BY atividade
    """, (id_etapa,)).fetchall()

    conn.close()

    return rows

def buscar_atividade(id_atividade):

    conn = get_connection()

    row = conn.execute("""
        SELECT
            id_atividade,
            atividade,
            id_etapa
        FROM tb_atividade
        WHERE id_atividade = ?
    """, (id_atividade,)).fetchone()

    conn.close()

    return row