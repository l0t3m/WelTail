#################### Imports: ####################

import db



#################### Functions: ####################

def getUserData(username):
    for user in db.get_TableDicts("SELECT * FROM users"):
        if user['username'] == username:
            return user
