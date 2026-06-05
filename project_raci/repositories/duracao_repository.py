from db import get_connection

def criar_duracao(
    id_projeto,
    id_atividade,
    duracao,
):
    conn = get_connection()

    conn.execute("""
        INSERT INTO tb_duracao (
            id_projeto,
            id_atividade,
            duracao
        )
        VALUES (?, ?, ?)
    """, (
        id_projeto,
        id_atividade,
        duracao,
    ))

    conn.commit()
    conn.close()