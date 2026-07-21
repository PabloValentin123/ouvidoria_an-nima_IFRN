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


def criar_tabelas():
    """
    Cria as tabelas do banco seguindo o modelo:

    CATEGORIA (id PK, nom_categoria)
    LOCAL (id PK, nome_local)
    RECLAMACAO (id PK, titulo, descricao, data_criacao, status,
                categoria_id FK -> categoria.id,
                local_id FK -> local.id)
    """
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS categoria(
            id SERIAL PRIMARY KEY,
            nom_categoria VARCHAR(50) UNIQUE NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS local(
            id SERIAL PRIMARY KEY,
            nome_local VARCHAR(100) UNIQUE NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reclamacao(
            id SERIAL PRIMARY KEY,
            titulo VARCHAR(100) NOT NULL,
            descricao TEXT NOT NULL,
            data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(30) NOT NULL DEFAULT 'Aberta',
            categoria_id INTEGER NOT NULL REFERENCES categoria(id),
            local_id INTEGER NOT NULL REFERENCES local(id)
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


def _obter_ou_criar_categoria(cur, nome):
    cur.execute(
        "SELECT id FROM categoria WHERE nom_categoria = %s",
        (nome,)
    )
    linha = cur.fetchone()

    if linha:
        return linha[0]

    cur.execute(
        "INSERT INTO categoria (nom_categoria) VALUES (%s) RETURNING id",
        (nome,)
    )
    return cur.fetchone()[0]


def _obter_ou_criar_local(cur, nome):
    cur.execute(
        "SELECT id FROM local WHERE nome_local = %s",
        (nome,)
    )
    linha = cur.fetchone()

    if linha:
        return linha[0]

    cur.execute(
        "INSERT INTO local (nome_local) VALUES (%s) RETURNING id",
        (nome,)
    )
    return cur.fetchone()[0]


def inserir(titulo, descricao, categoria, local):
    conn = conectar()
    cur = conn.cursor()

    categoria_id = _obter_ou_criar_categoria(cur, categoria)
    local_id = _obter_ou_criar_local(cur, local)

    cur.execute("""
        INSERT INTO reclamacao
        (titulo, descricao, categoria_id, local_id)
        VALUES (%s, %s, %s, %s)
    """, (
        titulo,
        descricao,
        categoria_id,
        local_id
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
        SELECT
            r.id,
            r.titulo,
            r.descricao,
            r.data_criacao,
            r.status,
            c.nom_categoria AS categoria,
            l.nome_local AS local
        FROM reclamacao r
        JOIN categoria c ON r.categoria_id = c.id
        JOIN local l ON r.local_id = l.id
        ORDER BY r.id DESC
    """)

    dados = cur.fetchall()

    cur.close()
    conn.close()

    return dados


def atualizar_status(id, status):
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        UPDATE reclamacao
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
        DELETE FROM reclamacao
        WHERE id = %s
    """, (id,))

    conn.commit()
    cur.close()
    conn.close()
