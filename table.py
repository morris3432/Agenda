import sqlite3 as sql

conn=sql.connect('datos.db')

c=conn.cursor()

c.execute('''
          CREATE TABLE datos(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              nombre TEXT NOT NULL,
              edad INTEGER NOT NULL,
              correo TEXT NOT NULL,
              telefono INTEGER NOT NULL
          )
          
          ''')

conn.commit()

conn.close()