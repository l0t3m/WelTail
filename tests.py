import functions, db

def setup_TestData(filename:str="weltail.db"):
    '''Creates a default data to test with.'''
    db.query("INSERT INTO users (username, fullname, password) VALUES ('lotem', 'lotem', '1212')", filename)

    db.query("INSERT INTO pets (user_id, species, name, gender, birthDate, race) VALUES ('1', 'cat', 'Hatol', 'male', '2019-10-10', 'Scottish Straight');", filename)
    db.query("INSERT INTO pets (user_id, species, name, gender, birthDate, race) VALUES ('1', 'cat', 'Mini', 'male', '2000-11-13', 'Turkish Angora');", filename)
    db.query("INSERT INTO pets (user_id, species, name, gender, birthDate, race) VALUES ('1', 'dog', 'Koda', 'male', '2019-02-02', 'Samoyed');", filename)

    db.query(f"INSERT INTO activities (user_id, pet_id, type, name, repeat, nextAlert, repeatInterval) VALUES ('1', '3', 'Exercise', 'Walk Koda', 1, '{functions.generate_firstAlert(600)}', '43200');", filename)
    db.query(f"INSERT INTO activities (user_id, pet_id, type, name, repeat, nextAlert, repeatInterval) VALUES ('1', '1', 'Food', 'Feed Hatol', 1, '{functions.generate_firstAlert(600)}', '21600');", filename)
    db.query(f"INSERT INTO activities (user_id, pet_id, type, name, repeat, nextAlert, repeatInterval) VALUES ('1', '2', 'Food', 'Feed Mini, 1 day', 1, '{functions.generate_firstAlert(600)}', '86400');", filename)
    db.query(f"INSERT INTO activities (user_id, pet_id, type, name, repeat, nextAlert, repeatInterval) VALUES ('1', '2', 'Treat', 'Give treat to Mini, 4 days', 0, '{functions.generate_firstAlert(600)}', '345600');", filename)