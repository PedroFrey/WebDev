from db import get_connection

def listar_alocacoes():

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            a.id_projeto,
            p.projeto,

            a.id_atividade,
            at.atividade,
            at.id_etapa,

            a.id_raci,
            l.desc_raci,

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

        ORDER BY
            p.projeto,
            at.atividade
    """).fetchall()

    conn.close()

    return rows

def criar_alocacao(
    id_projeto,
    id_atividade,
    id_raci,
    id_area,
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
        id_area,
    ))

    conn.commit()
    conn.close()

def excluir_alocacao(
    id_projeto,
    id_atividade,
    id_raci,
    id_area,
):
    conn = get_connection()

    conn.execute("""
        DELETE FROM tb_alocacao
        WHERE id_projeto = ?
          AND id_atividade = ?
          AND id_raci = ?
          AND id_area = ?
    """, (
        id_projeto,
        id_atividade,
        id_raci,
        id_area,
    ))

    conn.commit()
    conn.close()

def atualizar_alocacao(
    old_id_projeto,
    old_id_atividade,
    old_id_raci,
    old_id_area,

    id_projeto,
    id_atividade,
    id_raci,
    id_area,
):
    conn = get_connection()

    conn.execute("""
        UPDATE tb_alocacao
        SET
            id_projeto = ?,
            id_atividade = ?,
            id_raci = ?,
            id_area = ?
        WHERE id_projeto = ?
          AND id_atividade = ?
          AND id_raci = ?
          AND id_area = ?
    """, (
        id_projeto,
        id_atividade,
        id_raci,
        id_area,

        old_id_projeto,
        old_id_atividade,
        old_id_raci,
        old_id_area,
    ))

    conn.commit()
    conn.close()

