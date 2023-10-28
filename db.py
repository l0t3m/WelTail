#################### Imports: ####################

import sqlite3, os



#################### Main Functions: ####################

def setup():
    if not os.path.exists('weltail.db'):
        query("""CREATE TABLE IF NOT EXISTS "users" ("user_id" INTEGER PRIMARY KEY,"username" TEXT,"password" TEXT); """)
        query("""CREATE TABLE IF NOT EXISTS "pets" (
              "user_id" INTEGER, "pet_id" INTEGER PRIMARY KEY, 
              "pet_species"	TEXT, "pet_sex" TEXT, "pet_birthDate" TEXT, "pet_race" TEXT, 
              FOREIGN KEY ("user_id") REFERENCES users ("user_id")); """)


def query(sql, filename="weltail.db"):
    with sqlite3.connect(filename) as conn:
        cur = conn.cursor()
        rows = cur.execute(sql).fetchall()
        return rows





