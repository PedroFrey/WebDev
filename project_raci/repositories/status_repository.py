from db import get_connection


def listar_status():

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            id_projeto,
            id_atividade,
            dt_inicio_real,
            dt_inicio_previsto,
            dt_fim_real,
            dt_fim_previsto
        FROM tb_status
    """).fetchall()

    conn.close()

    return rows
