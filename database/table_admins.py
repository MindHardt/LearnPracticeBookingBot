import sqlite3
connection = sqlite3.connect('h.db')
cursor = connection.cursor()

def add_admin(user_id):
    cursor.execute("insert into admins(id_admin) values(?)", user_id)
    connection.commit()    
    return


def revoke_admin(user_id):
    cursor.execute(f"delete from admins where id_admin = {user_id}")
    connection.commit() 
    return


def is_admin(user_id) -> bool:  
    admin_id = [x[0] for x in cursor.execute(f"select id_admin from admins where id_admin = {user_id}").fetchall()]
    if len(admin_id) != 0:
        print('есть')
    else:
        print('Нет')


def create_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS admins(id_admin INTEGER, comment TEXT)")
    connection.commit() 
    return

user_id = '6'
create_table()
add_admin(user_id)
revoke_admin(user_id)
is_admin(user_id)
