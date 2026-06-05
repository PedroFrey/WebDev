from db import get_connection


def listar_responsaveis():

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            r.id_responsavel,
            r.responsavel,
            r.id_area,
            a.area
        FROM tb_responsavel r
        JOIN tb_area a
            ON r.id_area = a.id_area
        ORDER BY r.responsavel
    """).fetchall()

    conn.close()

    return rows


def criar_responsavel(nome, id_area):

    conn = get_connection()

    conn.execute("""
        INSERT INTO tb_responsavel
        (id_area, responsavel)
        VALUES (?, ?)
    """, (
        id_area,
        nome
    ))

    conn.commit()
    conn.close()


def atualizar_responsavel(
    id_responsavel,
    nome,
    id_area
):

    conn = get_connection()

    conn.execute("""
        UPDATE tb_responsavel
        SET
            responsavel = ?,
            id_area = ?
        WHERE id_responsavel = ?
    """, (
        nome,
        id_area,
        id_responsavel
    ))

    conn.commit()
    conn.close()


def excluir_responsavel(id_responsavel):

    conn = get_connection()

    conn.execute("""
        DELETE FROM tb_responsavel
        WHERE id_responsavel = ?
    """, (id_responsavel,))

    conn.commit()
    conn.close()
