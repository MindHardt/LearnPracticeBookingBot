class EntityUser:
    unique_id = str  # VARCHAR(36), PK
    name = str  # VARCHAR(36)
    balance = int  # INTEGER
    login = str  # VARCHAR(36), UNIQUE
    password_hash = int  # INTEGER
    
     def __create_table__():
        cursor.execute("PRAGMA foreign_keys=on")
        cursor.execute("CREATE TABLE IF NOT EXISTS EntityRequest(location_lon NUMERIC(10), "
                       "location_lat NUMERIC(10), date_arrive DATETIME, date_depart DATETIME, "
                       "date_request DATETIME, optional_filters TEXT,REFERENCES flight(id_number_trip),"
                       "FOREIGN KEY (user_id) REFERENCES EntityUser(unique_id))")
        connection.commit()
