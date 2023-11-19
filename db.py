#################### Imports: ####################

import sqlite3, os, functions, tests



#################### Main Functions: ####################

def query(sql:str="SELECT * FROM users", filename:str="weltail.db"):
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


def get_TableKeys(sql:str="SELECT * FROM users", filename:str="weltail.db"):
    with sqlite3.connect(filename) as conn:
        cur = conn.cursor().execute(sql)
        conn.commit()

        row_names = []
        for row in cur.description:
            row_names.append(row[0])
        return row_names


def get_TableDicts(sql:str="SELECT * FROM users", filename:str="weltail.db"):
    rows = query(sql, filename)["rows"]
    keys = query(sql, filename)["keys"]

    cell_data = []
    for cell in rows:
        values = list(cell)
        row_dict = dict(zip(keys, values))
        cell_data.append(row_dict)
    return cell_data



#################### Setup: ####################

def setup(filename:str="weltail.db", testData:bool=True):
    if not os.path.exists(filename):
        query("""CREATE TABLE IF NOT EXISTS "users" ("user_id" INTEGER PRIMARY KEY,"username" TEXT, "fullname" TEXT, "password" TEXT);""", filename)
        query("""CREATE TABLE IF NOT EXISTS "pets" 
              ("user_id" INTEGER, "pet_id" INTEGER PRIMARY KEY, "species" TEXT, "name" TEXT, "gender" TEXT, "birthDate" TEXT, "race" TEXT, 
              FOREIGN KEY ("user_id") REFERENCES users ("user_id"));""", filename)
        query("""CREATE TABLE IF NOT EXISTS "activities" 
              ("user_id" INTEGER, "pet_id" INTEGER, "activity_id" INTEGER PRIMARY KEY, 
              "type" TEXT, "name" TEXT, "repeat" INT, "nextAlert" TEXT, "repeatInterval" TEXT,
              FOREIGN KEY ("user_id", "pet_id") REFERENCES pets ("user_id", "pet_id"));""", filename)
       
        if testData == True:
            tests.setup_TestData(filename=filename)
