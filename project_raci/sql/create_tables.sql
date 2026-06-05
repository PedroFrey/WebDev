CREATE TABLE IF NOT EXISTS tb_etapa (
    id_etapa INTEGER PRIMARY KEY,
    etapa TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_atividade (
    id_atividade INTEGER PRIMARY KEY,
    id_etapa INTEGER NOT NULL,
    atividade TEXT NOT NULL,

    FOREIGN KEY (id_etapa)
        REFERENCES tb_etapa(id_etapa)
);

CREATE TABLE IF NOT EXISTS tb_business_unit (
    cliente_id INTEGER PRIMARY KEY,
    cliente TEXT NOT NULL,
    bu TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_area (
    id_area INTEGER PRIMARY KEY,
    area TEXT NOT NULL,
    empresa TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_projeto (
    id_projeto INTEGER PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    projeto TEXT NOT NULL,

    FOREIGN KEY (cliente_id)
        REFERENCES tb_business_unit(cliente_id)
);

CREATE TABLE IF NOT EXISTS tb_legenda_raci (
    id_raci INTEGER PRIMARY KEY,
    legenda_raci TEXT NOT NULL,
    desc_raci TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_responsavel (
    id_responsavel INTEGER PRIMARY KEY,
    id_area INTEGER NOT NULL,
    responsavel TEXT NOT NULL,

    FOREIGN KEY (id_area)
        REFERENCES tb_area(id_area)
);

CREATE TABLE IF NOT EXISTS tb_dependencias (
    id_atividade_pai INTEGER NOT NULL,
    id_atividade_filho INTEGER NOT NULL,

    PRIMARY KEY (
        id_atividade_pai,
        id_atividade_filho
    ),

    FOREIGN KEY (id_atividade_pai)
        REFERENCES tb_atividade(id_atividade),

    FOREIGN KEY (id_atividade_filho)
        REFERENCES tb_atividade(id_atividade)
);

CREATE TABLE IF NOT EXISTS tb_duracao (
    id_projeto INTEGER NOT NULL,
    id_atividade INTEGER NOT NULL,
    duracao INTEGER NOT NULL,

    PRIMARY KEY (
        id_projeto,
        id_atividade
    ),

    FOREIGN KEY (id_projeto)
        REFERENCES tb_projeto(id_projeto),

    FOREIGN KEY (id_atividade)
        REFERENCES tb_atividade(id_atividade)
);

CREATE TABLE IF NOT EXISTS tb_status (
    id_projeto INTEGER NOT NULL,
    id_atividade INTEGER NOT NULL,

    dt_inicio_real DATE,
    dt_inicio_previsto DATE,
    dt_fim_real DATE,
    dt_fim_previsto DATE,

    PRIMARY KEY (
        id_projeto,
        id_atividade
    ),

    FOREIGN KEY (id_projeto)
        REFERENCES tb_projeto(id_projeto),

    FOREIGN KEY (id_atividade)
        REFERENCES tb_atividade(id_atividade)
);

CREATE TABLE IF NOT EXISTS tb_alocacao (
    id_projeto INTEGER NOT NULL,
    id_atividade INTEGER NOT NULL,
    id_raci INTEGER NOT NULL,
    id_area INTEGER NOT NULL,

    PRIMARY KEY (
        id_projeto,
        id_atividade,
        id_raci
    ),

    FOREIGN KEY (id_projeto)
        REFERENCES tb_projeto(id_projeto),

    FOREIGN KEY (id_atividade)
        REFERENCES tb_atividade(id_atividade),

    FOREIGN KEY (id_raci)
        REFERENCES tb_legenda_raci(id_raci),

    FOREIGN KEY (id_area)
        REFERENCES tb_area(id_area)
);