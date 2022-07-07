class EntityUser:
    unique_id = str  # VARCHAR(36), PK
    name = str  # VARCHAR(36)
    balance = int  # INTEGER
    login = str  # VARCHAR(36), UNIQUE
    password_hash = int  # INTEGER
    
    def __create_table__():
    cursor.execute("PRAGMA foreign_keys=on")
    cursor.execute("CREATE TABLE IF NOT EXISTS EntityUser(unique_id VARCHAR(36) PRIMARY KEY, "
                       "name VARCHAR(36), balance INTEGER, login VARCHAR(36) UNIQUE, "
                       "password_hash INTEGER")
    connection.commit()
