import sqlite3

HOST = ''
PORT = 1024

def initialise_database():
    connection = sqlite3.connect('registry.db')
    cursor = connection.cursor()

    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS certificate_authority(
    ID INTEGER PRIMARY KEY,
    public_key TEXT,
    mac_address TEXT
    )
    """)

    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS registered_entities(
    ID INTEGER PRIMARY KEY,
    entity_type TEXT,
    mac_address TEXT
    )
    """)

    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS private_lookup(
    UAS_ID INTEGER PRIMARY KEY,
    Entity_ID INTEGER,
    Registry_ID INTEGER,
    Serial_Num TEXT
    )
    """)

    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS public_lookup(
    UAS_ID INTEGER PRIMARY KEY,
    operator_name TEXT,
    emergency_num INTEGER,
    date_of_birth TEXT
    )
    """)

    connection.commit()
    return

def run():
    return

if __name__ == '__main__':
    initialise_database()
    run()