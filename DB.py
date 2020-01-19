import sqlite3



def create():
    try:
        conn = sqlite3.connect('registro.db')
        cursor = conn.cursor()
        cursor.execute(

            """CREATE TABLE registro(
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
        print('tabela criada com sucesso')
        conn.close()
    except:
        pass


def insert(*args):
    conn = sqlite3.connect('registro.db')
    cursos = conn.cursor()
    cursos.execute("""INSERT INTO registro(quedahora,quedadata,voltahora,voltadata,tempo,down,up,ping,
    clima) VALUES(?,?,?,?,?,?,?,?,?)""", *args)
    conn.commit()
    print('Salvo')
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
