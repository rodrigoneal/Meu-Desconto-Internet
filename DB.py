import sqlite3


def insert(*args):
    conn = sqlite3.connect('registro.db')
    cursos = conn.cursor()
    cursos.executemany("""INSERT INTO registro(queda,volta,tempo,down,up,ping,clima) VALUES(?,?,?,?,?,?,?)""", args)
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