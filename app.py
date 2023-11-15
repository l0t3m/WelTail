#################### Imports: ####################

from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)

import db, functions



#################### Variables: ####################

db.setup()
app.secret_key = "_WilTail_"



#################### Routes: ####################

@app.route('/', methods=['GET'])
def home():
    if session.get('user_id', "") == "":
        return render_template("home.html")
    return redirect(f"/feed/{session['user_id']}")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html", message="")

    for user in db.get_TableDicts("SELECT * FROM users"):
        if user['username'].lower() == request.form['username'].lower() and user['password'] == request.form['password']:
            session['user_id'] = user['user_id']
            return redirect(f"/feed/{user['user_id']}")

    return render_template("login.html", message="Incorrect username / password")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    
    db.query(f"INSERT INTO users (username, password) VALUES ('{request.form['username']}', '{request.form['password']}');")
    session['user_id'] = functions.getUserData(request.form['username'])['user_id']
    return redirect(f"/feed/{session['user_id']}")


@app.route('/feed/<user_id>', methods=['GET'])
def feed(user_id):
    if session.get('user_id', "") == "":
        return redirect("/")
    
    if session['user_id'] == int(user_id):
        return render_template("feed.html")

    return redirect("/feed")


@app.route('/profile/<user_id>', methods=['GET'])
def profile(user_id):
    if session.get('user_id', "") == "":
        return redirect("/")
    
    if session['user_id'] == int(user_id):
        return render_template("profile.html", user_id=user_id, pets = db.get_TableDicts(f"SELECT * FROM pets WHERE user_id = '{user_id}';"))
    
    return redirect("/profile")


@app.route('/petprofile/<user_id>/<pet_id>', methods=['GET'])
def petProfile(user_id, pet_id):
    if session.get('user_id', "") == "":
        return redirect("/")
    if session['user_id'] == int(user_id):
        return render_template("petProfile.html", user_id=user_id, pet=db.get_TableDicts(f"SELECT * FROM pets WHERE user_id = '{user_id}' AND pet_id = '{pet_id}';"), activities=functions.reformat_activities(functions.getPetActivities(user_id, pet_id)) )
        
    return redirect("/profile")


@app.route('/logout', methods=['GET'])
def logout():
    if session.get('user_id', "") == "":
        return redirect("/")
    session.clear()
    return redirect("/")



#################### Action Routes: ####################

@app.route('/pet/add/<user_id>', methods=['GET','POST'])
def pet_add(user_id):
    if session.get('user_id', "") == "" or int(user_id) != session['user_id']:
        return redirect('/')

    if request.method == "GET":
        return render_template("addPet.html", user_id = user_id)
    
    db.query(f"INSERT INTO pets (user_id, species, name, gender, birthDate, race) VALUES ('{user_id}', '{request.form['species']}', '{request.form['name']}', '{request.form['gender']}', '{request.form['birthDate']}', '{request.form['race']}');")
    return redirect('/profile')


@app.route('/pet/delete/<user_id>/<pet_id>', methods=['GET'])
def pet_delete(user_id, pet_id):
    if session.get('user_id', "") == "" or int(user_id) != session['user_id']:
        return redirect('/')

    db.query(f"DELETE FROM pets WHERE user_id = '{user_id}' AND pet_id = '{pet_id}';")
    db.query(f"DELETE FROM activities WHERE pet_id = {pet_id};")
    return redirect('/profile')


@app.route('/pet/edit/<user_id>/<pet_id>', methods=['GET', 'POST'])
def pet_edit(user_id, pet_id):
    if session.get('user_id', "") == "" or int(user_id) != session['user_id']:
        return redirect('/')

    if request.method == 'GET':
        return render_template('editPet.html', pet = db.get_TableDicts(f"SELECT * FROM pets WHERE pet_id = '{pet_id}';"))

    db.query(f"UPDATE pets SET species='{request.form['species']}', name='{request.form['name']}', gender='{request.form['gender']}', birthDate='{request.form['birthDate']}', race='{request.form['race']}' WHERE pet_id='{pet_id}';")
    return redirect(f'/petprofile/{user_id}/{pet_id}')


@app.route('/activity/add/<user_id>/<pet_id>', methods=['GET','POST'])
def activity_add(user_id, pet_id):
    if session.get('user_id', "") == "" or int(user_id) != session['user_id']:
        return redirect('/')
    
    if request.method == 'GET':
        return render_template("addActivity.html", user_id = user_id, pet_id = pet_id)

    functions.addActivity(user_id, pet_id, request.form['type'], request.form['name'], request.form['nextAlert'], request.form['repeat'], request.form['repeatType'], request.form['repeatAmount'])
    
    return redirect(f'/petprofile/{user_id}/{pet_id}')


@app.route('/activity/delete/<user_id>/<activity_id>', methods=['GET'])
def activity_delete(user_id, activity_id):
    if session.get('user_id', "") == "" or int(user_id) != session['user_id']:
        return redirect('/')
    
    db.query(f"DELETE FROM activities WHERE user_id = '{user_id}' AND activity_id = '{activity_id}';")
    return redirect('/profile')


@app.route('/activity/done/<user_id>/<activity_id>', methods=['GET'])
def activity_done(user_id, activity_id):
    if session.get('user_id', "") == "" or int(user_id) != session['user_id']:
        return redirect('/')
    
    functions.activity_done(activity_id)
    return redirect('/feed')


@app.route('/activity/edit/<user_id>/<activity_id>', methods=['GET', 'POST'])
def activity_edit(user_id, activity_id):
    if session.get('user_id', "") == "" or int(user_id) != session['user_id']:
        return redirect('/')
    
    if request.method == 'GET':
        session['activity'] = functions.deformat_activity(db.get_TableDicts(f"SELECT * FROM activities WHERE activity_id = {activity_id};")[0])
        return render_template('editActivity.html', activity=session['activity'])

    functions.updateActivity(session['activity']['activity_id'], request.form['type'], request.form['name'], request.form['nextAlert'], request.form['repeat'], request.form['repeatType'], request.form['repeatAmount'])

    session.pop('activity', default=None)
    return redirect("/feed")



#################### Redirect Routes: ####################

@app.route('/feed')
def redirect_feed():
    if session.get('user_id', "") == "":
        return redirect("/")
    return redirect(f"/feed/{session['user_id']}")


@app.route('/profile')
def redirect_profile():
    if session.get('user_id', "") == "":
        return redirect("/")
    return redirect(f"/profile/{session['user_id']}")



#################### API Routes: ####################

@app.route('/api/myUser')
def myUser():
    if session.get('user_id', "") == "":
        return ""

    return db.get_TableDicts(f"SELECT * FROM users WHERE user_id = {session['user_id']}")[0]


@app.route('/api/myPets')
def myPets():
    if session.get('user_id', "") == "":
        return ""
    
    return db.get_TableDicts(f"SELECT * FROM pets WHERE user_id = {session['user_id']}")


@app.route('/api/myActivities')
def myActivities():
    if session.get('user_id', "") == "":
        return ""
    return functions.reformat_activities(db.get_TableDicts(f"SELECT * FROM activities WHERE user_id = {session['user_id']} ORDER BY nextAlert;"))


@app.route('/api/myUpcomingActivities')
def myUpcomingActivities():
    if session.get('user_id', "") == "":
        return ""
    return functions.reformat_activities(functions.getUpcomingAlerts(session['user_id']))


@app.route('/api/getTargetedActivity')
def getTargetedActivity():
    '''Returns the last activity targeted. Used in Edit Activity.'''
    if session.get('user_id', "") == "":
        return ""
    try:
        return session['activity']
    except:
        return []


@app.route('/api/allUsernames')
def viewUsernames():
    usernames = []
    for user in db.get_TableDicts("SELECT * FROM users"):
        usernames.append(user['username'])
    return usernames


@app.route('/api/greetingMessage')
def greetingMessage():
    '''Returns a greeting message according to the current time.'''
    return functions.generate_greetingMessage()



#################### Temp Routes: ####################

@app.route('/users')
def users():
    users = []
    for user in db.get_TableDicts("SELECT * FROM users"):
        users.append(user)
    return users


@app.route('/pets')
def pets():
    pets = []
    for pet in db.get_TableDicts("SELECT * FROM pets"):
        pets.append(pet)
    return pets


@app.route('/activities')
def activities():
    activities = []
    for activity in db.get_TableDicts("SELECT * FROM activities"):
        activities.append(activity)
    return activities


@app.route('/test')
def test():
    activities = []

    for user in db.get_TableDicts("SELECT user_id FROM users"):
        functions.updateUserAlerts(user['user_id'])

    for activity in db.get_TableDicts("SELECT * FROM activities"):
        secondsLeft = functions.generateCountdown(int(activity['nextAlert']))

        tempd = {
            "NAME" : activity['name'],
            "seconds left" : secondsLeft,
            "minutes left" : secondsLeft // 60 if secondsLeft > 60 else "less than a minute",
        }
        activities.append(tempd)

    return activities

