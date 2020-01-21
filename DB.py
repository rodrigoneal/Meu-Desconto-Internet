import sqlite3
from datetime import datetime
import DB
from conexao import Requisicao


def create():
    try:
        conn = sqlite3.connect('registro.db')
        cursor = conn.cursor()
        cursor.execute(

            """CREATE TABLE IF NOT EXISTS registro(
        quedahora DATETIME NOT NULL,
        quedadata DATETIME NOT NULL,
        voltahora DATETIME NOT NULL,
        voltadata DATETIME NOT NULL,
        tempo DATETIME NOT NULL,
        down INT ,
        up INT ,
        ping INT ,
        clima TEXT
    );""")
        conn.close()
    except:
        pass


def insert(*args):
    conn = sqlite3.connect('registro.db')
    cursos = conn.cursor()
    cursos.execute("""INSERT INTO registro(quedahora,quedadata,voltahora,voltadata,tempo,down,up,ping,
    clima) VALUES(?,?,?,?,?,?,?,?,?)""", *args)
    conn.commit()
    conn.close()


def select(propriedade):
    conn = sqlite3.connect('registro.db')
    cursos = conn.cursor()
    cursos.execute("SELECT {} FROM registro".format(propriedade))
    resultado = cursos.fetchall()
    conn.commit()
    conn.close()
    return resultado


def where(select, where, igual):
    conn = sqlite3.connect('registro.db')
    cursos = conn.cursor()
    cursos.execute("SELECT {} FROM registro WHERE {} = '{}'".format(select, where, igual))
    resultado = cursos.fetchall()
    conn.commit()
    conn.close()
    return resultado


def controleMes():
    ano = datetime.now().year
    conn = sqlite3.connect(f'{ano}.db')
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS desconto(
    Janeiro REAL,
    fevereiro REAL,
    marco REAL,
    abril REAL,
    maio REAL,
    junho REAL,
    julho REAL,
    agosto REAL,
    setembro REAL,
    outubro REAL,
    novembro REAL,
    dezembro REAL
    );""")
    conn.close()


def update(banco, tabela, coluna, valor):
    conn = sqlite3.connect(f'{banco}.db')
    cursos = conn.cursor()
    cursos.execute("""UPDATE '{}' SET '{}' = '{}'""".format(tabela, coluna, valor))
    conn.commit()
    conn.close()


def desconto():
    from calendar import month_name
    requisicao = Requisicao('url')
    desconto1 = requisicao.desconto()
    mes_db = month_name[desconto1[1]]

    DB.update('2020', 'desconto', mes_db, desconto1[0])