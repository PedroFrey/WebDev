from db import get_connection


def listar_alocacoes():

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            a.id_projeto,
            p.projeto,

            a.id_atividade,
            at.atividade,

            a.id_raci,
            l.legenda_raci,

            a.id_area,
            ar.area

        FROM tb_alocacao a

        JOIN tb_projeto p
            ON p.id_projeto = a.id_projeto

        JOIN tb_atividade at
            ON at.id_atividade = a.id_atividade

        JOIN tb_legenda_raci l
            ON l.id_raci = a.id_raci

        JOIN tb_area ar
            ON ar.id_area = a.id_area

        ORDER BY p.projeto, at.atividade
    """).fetchall()

    conn.close()

    return rows


def criar_alocacao(
    id_projeto,
    id_atividade,
    id_raci,
    id_area
):

    conn = get_connection()

    conn.execute("""
        INSERT INTO tb_alocacao (
            id_projeto,
            id_atividade,
            id_raci,
            id_area
        )
        VALUES (?, ?, ?, ?)
    """, (
        id_projeto,
        id_atividade,
        id_raci,
        id_area
    ))

    conn.commit()
    conn.close()


def excluir_alocacao(
    id_projeto,
    id_atividade
):

    conn = get_connection()

    conn.execute("""
        DELETE FROM tb_alocacao
        WHERE id_projeto = ?
          AND id_atividade = ?
    """, (
        id_projeto,
        id_atividade
    ))

    conn.commit()
    conn.close()
