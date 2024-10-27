import sqlite3 

class ContactManager:
    def __init__(self) -> None:
        self.connection=sqlite3.connect('datos.db',check_same_thread=False)
        
        
    def  adds(self, name, edad, email, phone):
        query = '''insert into datos (nombre, edad, correo, telefono)
                    values (?,?,?,?)
                '''
        self.connection.execute(query, (name, edad, email, phone))
        self.connection.commit()
            
    def get_contact(self):
        cursor = self.connection.cursor()
        query = 'select * from datos'
        cursor.execute(query)
        contacts=cursor.fetchall()
        return contacts
        
    def delete__contacts(self, name):
        query = '''delete from datos
                   where nombre=?
                '''
        self.connection.execute(query,(name, ))
        self.connection.commit()
            
    def update__contact(self, contact_id, name, edad, email, phone):
        query = 'update datos set nombre=?, edad=?, correo=?, telefono=? where id=?'
        self.connection.execute(query, (name, edad, email, phone, contact_id))
        self.connection.commit()
            
    def close_conect(self):
        self.connection.close()       
