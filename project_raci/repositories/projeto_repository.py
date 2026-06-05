from db import get_connection


def listar_projetos():

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            p.id_projeto,
            p.projeto,
            b.cliente
        FROM tb_projeto p
        JOIN tb_business_unit b
            ON p.cliente_id = b.cliente_id
        ORDER BY p.projeto
    """).fetchall()

    conn.close()

    return rows


def criar_projeto(cliente_id, projeto):

    conn = get_connection()

    conn.execute("""
        INSERT INTO tb_projeto
        (cliente_id, projeto)
        VALUES (?, ?)
    """, (
        cliente_id,
        projeto
    ))

    conn.commit()
    conn.close()


def atualizar_projeto(
    id_projeto,
    cliente_id,
    projeto
):

    conn = get_connection()

    conn.execute("""
        UPDATE tb_projeto
        SET
            cliente_id = ?,
            projeto = ?
        WHERE id_projeto = ?
    """, (
        cliente_id,
        projeto,
        id_projeto
    ))

    conn.commit()
    conn.close()


def excluir_projeto(id_projeto):

    conn = get_connection()

    conn.execute("""
        DELETE FROM tb_projeto
        WHERE id_projeto = ?
    """, (id_projeto,))

    conn.commit()
    conn.close()
