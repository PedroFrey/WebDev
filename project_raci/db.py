import sqlite3
import os

DB_PATH = "database.db"

print("DB_PATH:", os.path.abspath(DB_PATH))

SEED_FILES = [
    "sql/seed_etapas.sql",
    "sql/seed_legenda_raci.sql",
    "sql/seed_area.sql",
    "sql/seed_business_unit.sql",
    "sql/seed_atividade.sql",
]


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():
    conn = get_connection()

    with open("sql/create_tables.sql", encoding="utf-8") as f:
        conn.executescript(f.read())

    for file in SEED_FILES:
        with open(file, encoding="utf-8") as f:
            conn.executescript(f.read())

    conn.commit()
    conn.close()