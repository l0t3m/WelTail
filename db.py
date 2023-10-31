#################### Imports: ####################

import sqlite3, os, functions



#################### Main Functions: ####################

def query(sql="SELECT * FROM users", filename="weltail.db"):
    with sqlite3.connect(filename) as conn:
        cur = conn.cursor().execute(sql)
        conn.commit()
        row_names = []
        try:
            for row in cur.description:
                row_names.append(row[0])
        except:
            row_names.append(get_TableKeys())
        return {"rows":cur.fetchall(), "keys":row_names}


def get_TableKeys(sql="SELECT * FROM users", filename="weltail.db"):
    with sqlite3.connect(filename) as conn:
        cur = conn.cursor().execute(sql)
        conn.commit()

        row_names = []
        for row in cur.description:
            row_names.append(row[0])
        return row_names


def get_TableDicts(sql="SELECT * FROM users", filename="weltail.db"):
    rows = query(sql, filename)["rows"]
    keys = query(sql, filename)["keys"]

    cell_data = []
    for cell in rows:
        values = list(cell)
        row_dict = dict(zip(keys, values))
        cell_data.append(row_dict)
    return cell_data



#################### Setup: ####################

def setup(filename="weltail.db"):
    if not os.path.exists('weltail.db'):
        query("""CREATE TABLE IF NOT EXISTS "users" ("user_id" INTEGER PRIMARY KEY,"username" TEXT,"password" TEXT);""", filename)
        query("""CREATE TABLE IF NOT EXISTS "pets" 
              ("user_id" INTEGER, "pet_id" INTEGER PRIMARY KEY, "species" TEXT, "name" TEXT, "gender" TEXT, "birthDate" TEXT, "race" TEXT, 
              FOREIGN KEY ("user_id") REFERENCES users ("user_id"));""", filename)
        query("""CREATE TABLE IF NOT EXISTS "activities" 
              ("user_id" INTEGER, "pet_id" INTEGER, "activity_id" INTEGER PRIMARY KEY, 
              "name" TEXT, "repeat" INT, "nextAlert" TEXT, "repeatInterval" TEXT,
              FOREIGN KEY ("user_id", "pet_id") REFERENCES pets ("user_id", "pet_id"));""", filename)
        
        setup_TestData()


def setup_TestData():
    query("INSERT INTO users (username, password) VALUES ('lotem', '1212')")
    query("INSERT INTO users (username, password) VALUES ('tohar', '5555')")

    query("INSERT INTO pets (user_id, species, name, gender, birthDate, race) VALUES ('1', 'cat', 'Haaaaatol', 'male', '2000-01-01', 'Scottish');")
    query("INSERT INTO pets (user_id, species, name, gender, birthDate, race) VALUES ('1', 'cat', 'Mini Hatol', 'male', '2000-01-01', 'Turkish');")
    query("INSERT INTO pets (user_id, species, name, gender, birthDate, race) VALUES ('2', 'dog', 'Lady', 'female', '2000-01-01', 'Malinois');")

    query(f"INSERT INTO activities (user_id, pet_id, name, repeat, nextAlert, repeatInterval) VALUES ('1', '1', '1 hour timer', 0, '{functions.generate_firstAlert(60)}', '3200');")
    query(f"INSERT INTO activities (user_id, pet_id, name, repeat, nextAlert, repeatInterval) VALUES ('1', '1', '10 minutes', 1, '1577829600', '600');")
    query(f"INSERT INTO activities (user_id, pet_id, name, repeat, nextAlert, repeatInterval) VALUES ('1', '1', '5 minutes', 1, '1577829600', '300');")
    query(f"INSERT INTO activities (user_id, pet_id, name, repeat, nextAlert, repeatInterval) VALUES ('1', '1', '10 seconds', 1, '1577829600', '10');")
    query(f"INSERT INTO activities (user_id, pet_id, name, repeat, nextAlert, repeatInterval) VALUES ('1', '1', '5 minutes', 0, '1577829600', '300');")
