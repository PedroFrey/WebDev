from db import get_connection


def listar_dependencias():

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            d.id_atividade_pai,
            pai.atividade AS atividade_pai,

            d.id_atividade_filho,
            filho.atividade AS atividade_filho

        FROM tb_dependencias d

        JOIN tb_atividade pai
            ON pai.id_atividade = d.id_atividade_pai

        JOIN tb_atividade filho
            ON filho.id_atividade = d.id_atividade_filho

        ORDER BY
            pai.atividade,
            filho.atividade
    """).fetchall()

    conn.close()

    return rows


def listar_dependencias_atividade(
    id_atividade
):

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            id_atividade_pai,
            id_atividade_filho
        FROM tb_dependencias
        WHERE id_atividade_pai = ?
           OR id_atividade_filho = ?
    """, (
        id_atividade,
        id_atividade,
    )).fetchall()

    conn.close()

    return rows


def criar_dependencia(
    id_atividade_pai,
    id_atividade_filho
):

    conn = get_connection()

    conn.execute("""
        INSERT OR IGNORE INTO tb_dependencias (
            id_atividade_pai,
            id_atividade_filho
        )
        VALUES (?, ?)
    """, (
        id_atividade_pai,
        id_atividade_filho,
    ))

    conn.commit()
    conn.close()


def excluir_dependencia(
    id_atividade_pai,
    id_atividade_filho
):

    conn = get_connection()

    conn.execute("""
        DELETE FROM tb_dependencias
        WHERE id_atividade_pai = ?
          AND id_atividade_filho = ?
    """, (
        id_atividade_pai,
        id_atividade_filho,
    ))

    conn.commit()
    conn.close()


def excluir_todas_dependencias_atividade(
    id_atividade
):

    conn = get_connection()

    conn.execute("""
        DELETE FROM tb_dependencias
        WHERE id_atividade_pai = ?
           OR id_atividade_filho = ?
    """, (
        id_atividade,
        id_atividade,
    ))

    conn.commit()
    conn.close()