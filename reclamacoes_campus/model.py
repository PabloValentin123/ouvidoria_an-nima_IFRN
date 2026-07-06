
import psycopg2
import psycopg2.extras
from psycopg2 import sql

HOST = "localhost"
PORT = "5432"
DB_NAME = "campus"
USER = "postgres"
PASSWORD = "postgres"


def criar_banco():
    conn = psycopg2.connect(
        host=HOST,
        port=PORT,
        dbname="postgres",
        user=USER,
        password=PASSWORD
    )

    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s",
        (DB_NAME,)
    )

    if cur.fetchone() is None:
        cur.execute(
            sql.SQL(
                "CREATE DATABASE {}"
            ).format(
                sql.Identifier(DB_NAME)
            )
        )

    cur.close()
    conn.close()


def conectar():
    return psycopg2.connect(
        host=HOST,
        port=PORT,
        dbname=DB_NAME,
        user=USER,
        password=PASSWORD
    )


def criar_tabela():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reclamacoes(
            id SERIAL PRIMARY KEY,
            titulo VARCHAR(100),
            descricao TEXT,
            categoria VARCHAR(50),
            local VARCHAR(100),
            status VARCHAR(30) DEFAULT 'Aberta'
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


def inserir(titulo, descricao, categoria, local):
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reclamacoes
        (titulo, descricao, categoria, local)
        VALUES (%s, %s, %s, %s)
    """, (
        titulo,
        descricao,
        categoria,
        local
    ))

    conn.commit()
    cur.close()
    conn.close()


def listar():
    conn = conectar()

    cur = conn.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )

    cur.execute("""
        SELECT * FROM reclamacoes
        ORDER BY id DESC
    """)

    dados = cur.fetchall()

    cur.close()
    conn.close()

    return dados


def atualizar_status(id, status):
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        UPDATE reclamacoes
        SET status = %s
        WHERE id = %s
    """, (status, id))

    conn.commit()
    cur.close()
    conn.close()


def excluir(id):
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM reclamacoes
        WHERE id = %s
    """, (id,))

    conn.commit()
    cur.close()
    conn.close()
