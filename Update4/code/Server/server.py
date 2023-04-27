import sqlite3
from fastapi import FastAPI
import string
import secrets

app = FastAPI()

# Create the database tables if they do not exist
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
    cursor.close()
    if connection:
        connection.close()
    return


@app.get('/get-registered-entities')
def get_registered_entities():
    connection = sqlite3.connect('registry.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * from registered_entities")
    result = cursor.fetchall()

    cursor.close()
    if connection:
        connection.close()
    return {"result" : result}

@app.get('/register-entity/{entity_type}/{mac_address}')
def register_entity(entity_type, mac_address):
    count = len(get_registered_entities()['result'])
    ID = count + 1

    connection = sqlite3.connect('registry.db')
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO registered_entities
    (ID, entity_type, mac_address)
    VALUES ({},'{}','{}')            
    """.format(ID, entity_type, mac_address))
    connection.commit()
    cursor.close()
    if connection:
        connection.close()
    return {"Success"}

@app.get('/add-private-info/{UAS_ID}/{entity_ID}/{registry_ID}/{serial_Num}')
def add_private_info(UAS_ID, entity_ID, registry_ID, serial_Num):
    connection = sqlite3.connect('registry.db')
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO private_lookup
    (UAS_ID, Entity_ID, Registry_ID, Serial_Num)
    VALUES ({},{},{},'{}')            
    """.format(UAS_ID, entity_ID, registry_ID, serial_Num))
    connection.commit()
    cursor.close()
    if connection:
        connection.close()
    return {"Success"}

@app.get('/add-public-info/{UAS_ID}/{operator_name}/{emergency_num}/{date_of_birth}')
def add_public_info(UAS_ID,operator_name,emergency_num,date_of_birth):
    connection = sqlite3.connect('registry.db')
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO public_lookup
    (UAS_ID, operator_name, emergency_num, date_of_birth)
    VALUES ({},'{}',{},'{}')            
    """.format(UAS_ID, operator_name, emergency_num, date_of_birth))
    connection.commit()
    cursor.close()
    if connection:
        connection.close()
    return {"Success"}

@app.get('/add-certifcate/{public_key}/{mac_address}')
def add_certificate(public_key, mac_address):
    connection = sqlite3.connect('registry.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * from certificate_authority")
    result = cursor.fetchall()
    count = len(result)
    ID_num = count + 1

    cursor.execute("""
    INSERT INTO certificate_authority
    (ID, public_key, mac_address)
    VALUES ({},'{}','{}')
    """.format(ID_num, public_key, mac_address))
    connection.commit()
    cursor.close()
    if connection:
        connection.close()
    return {"Success"}

@app.get('/public-lookup/{UAS_ID}')
def public_lookup(UAS_ID):
    connection = sqlite3.connect('registry.db')
    cursor = connection.cursor()
    cursor.execute(""" 
    SELECT * FROM public_lookup WHERE UAS_ID = {}
    """.format(UAS_ID))
    result = cursor.fetchall()
    cursor.close()
    if connection:
        connection.close()
    if len(result) != 0:
        return {"result" : result}
    else:
        return {"result" : "No information found."}

@app.get('/private-lookup/{UAS_ID}/{authentication_token}')
def private_lookup(UAS_ID, authentication_token):
    #validate authentication token here
    if int(authentication_token) > 0: #temporary test check
        connection = sqlite3.connect('registry.db')
        cursor = connection.cursor()
        cursor.execute("""
        SELECT * FROM private_lookup WHERE UAS_ID = {}
        """.format(UAS_ID))
        result = cursor.fetchall()
        cursor.close()
        if connection:
            connection.close()
        if len(result) != 0:
            return {"result" : result}
        else:
            return {"result" : "No information found"}
    else:
        return {"result" : "Not authorised to access this information."}

@app.get('/get-certificate/{mac_address}')
def get_certificate(mac_address):
    connection = sqlite3.connect('registry.db')
    cursor = connection.cursor()
    cursor.execute("""
    SELECT public_key FROM certificate_authority WHERE mac_address = '{}'
    """.format(mac_address))
    result = cursor.fetchall()
    cursor.close()
    if connection:
        connection.close()
    if len(result) != 0:
        return {"result" : result}
    else:
        return {"result" : "No certificate record found for {}".format(mac_address)}

@app.get('/check-certificate/{public_key}/{mac_address}')
def check_certificate(public_key, mac_address):
    connection = sqlite3.connect('registry.db')
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM certificate_authority WHERE mac_address = '{}' and public_key = '{}'
    """.format(mac_address, public_key))
    result = cursor.fetchall()
    cursor.close()
    if connection:
        connection.close()
    if len(result) > 0:
        return {"result" : "True"}
    else:
        return {"result" : "False"}

def run():
    print(generate_flight_session_key())
    return

def generate_flight_session_key():
    digits = string.ascii_uppercase + string.digits
    session_key = ''
    for _ in range(32):
        session_key += secrets.choice(digits)
    return session_key

if __name__ == '__main__':
    initialise_database()
    run()