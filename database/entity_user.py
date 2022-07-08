class EntityUser:
    unique_id = str  # VARCHAR(36), PK
    name = str  # VARCHAR(36)
    balance = 0  # INTEGER
    login = str  # VARCHAR(36), UNIQUE
    password_hash = str  # TEXT
