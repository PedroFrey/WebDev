from db import get_connection

conn = get_connection()
print(conn.execute("PRAGMA database_list").fetchall())
conn.close()

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


def criar_responsavel(nome, id_area):
    conn = get_connection()

    conn.execute("""
        INSERT INTO tb_responsavel
        (id_area, responsavel)
        VALUES (?, ?)
    """, (id_area, nome))

    conn.commit()
    conn.close()


def listar_responsaveis():
    conn = get_connection()

    rows = conn.execute("""
        SELECT
            r.id_responsavel,
            r.responsavel,
            a.area
        FROM tb_responsavel r
        JOIN tb_area a
            ON r.id_area = a.id_area
        ORDER BY r.responsavel
    """).fetchall()

    conn.close()

    return rows