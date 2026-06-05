from db import get_connection


def listar_etapas():

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            id_etapa,
            etapa
        FROM tb_etapa
        ORDER BY etapa
    """).fetchall()

    conn.close()

    return rows


def listar_areas():

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            id_area,
            area
        FROM tb_area
        ORDER BY area
    """).fetchall()

    conn.close()

    return rows


def listar_clientes():

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            cliente_id,
            cliente
        FROM tb_business_unit
        ORDER BY cliente
    """).fetchall()

    conn.close()

    return rows


def listar_legenda_raci():

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            id_raci,
            legenda_raci,
            desc_raci
        FROM tb_legenda_raci
        ORDER BY legenda_raci
    """).fetchall()

    conn.close()

    return rows


def listar_atividades():

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            a.id_etapa,
            a.id_atividade,
            a.atividade,
            e.etapa
        FROM tb_atividade a
        LEFT JOIN tb_etapa e
            ON e.id_etapa = a.id_etapa
        ORDER BY a.id_atividade
    """).fetchall()

    conn.close()

    return rows