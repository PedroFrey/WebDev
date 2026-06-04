from db import get_connection

# Listar Seeds
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
        SELECT cliente_id, cliente
        FROM tb_business_unit
        ORDER BY cliente
    """).fetchall()

    conn.close()
    return rows

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

def listar_alocacoes():
    conn = get_connection()

    rows = conn.execute("""
        SELECT
            a.id_projeto,
            p.projeto,

            a.id_atividade,
            at.atividade,

            a.id_responsavel,
            r.responsavel,

            a.id_raci,
            l.legenda_raci,

            a.id_area,
            ar.area

        FROM tb_alocacao a

        JOIN tb_projeto p
            ON p.id_projeto = a.id_projeto

        JOIN tb_atividade at
            ON at.id_atividade = a.id_atividade

        JOIN tb_responsavel r
            ON r.id_responsavel = a.id_responsavel

        JOIN tb_legenda_raci l
            ON l.id_raci = a.id_raci

        JOIN tb_area ar
            ON ar.id_area = a.id_area

        ORDER BY p.projeto, at.atividade
    """).fetchall()

    conn.close()
    return rows

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
# CRUD Responsáveis (Criar- Atualizar - Excluir)
def criar_responsavel(nome, id_area):
    conn = get_connection()

    conn.execute("""
        INSERT INTO tb_responsavel
        (id_area, responsavel)
        VALUES (?, ?)
    """, (id_area, nome))

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

def excluir_responsavel(
    id_responsavel
):
    conn = get_connection()

    conn.execute("""
        DELETE FROM tb_responsavel
        WHERE id_responsavel = ?
    """, (id_responsavel,))

    conn.commit()
    conn.close()

# CRUD Projetos (Criar- Atualizar - Excluir)

def criar_projeto(cliente_id, projeto):
    conn = get_connection()

    conn.execute("""
        INSERT INTO tb_projeto (cliente_id, projeto)
        VALUES (?, ?)
    """, (cliente_id, projeto))

    conn.commit()
    conn.close()

def atualizar_projeto(id_projeto, cliente_id, projeto):
    conn = get_connection()

    conn.execute("""
        UPDATE tb_projeto
        SET cliente_id = ?, projeto = ?
        WHERE id_projeto = ?
    """, (cliente_id, projeto, id_projeto))

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

# CRUD Alocações (Criar- Atualizar - Excluir)

def criar_alocacao(
    id_projeto,
    id_atividade,
    id_responsavel,
    id_raci,
    id_area
):
    conn = get_connection()

    conn.execute("""
        INSERT INTO tb_alocacao (
            id_projeto,
            id_atividade,
            id_responsavel,
            id_raci,
            id_area
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        id_projeto,
        id_atividade,
        id_responsavel,
        id_raci,
        id_area
    ))

    conn.commit()
    conn.close()

def atualizar_alocacao(
    id_projeto,
    id_atividade,
    id_responsavel,
    id_raci,
    id_area
):
    conn = get_connection()

    conn.execute("""
        UPDATE tb_alocacao
        SET
            id_responsavel = ?,
            id_raci = ?,
            id_area = ?
        WHERE id_projeto = ?
          AND id_atividade = ?
    """, (
        id_responsavel,
        id_raci,
        id_area,
        id_projeto,
        id_atividade
    ))

    conn.commit()
    conn.close()

def excluir_alocacao(id_projeto, id_atividade):
    conn = get_connection()

    conn.execute("""
        DELETE FROM tb_alocacao
        WHERE id_projeto = ?
          AND id_atividade = ?
    """, (id_projeto, id_atividade))

    conn.commit()
    conn.close()