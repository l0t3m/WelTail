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
        return render_template("feed.html", activities = db.get_TableDicts(f"SELECT * FROM activities WHERE user_id = {user_id}"))

    return redirect("/feed")


@app.route('/profile/<user_id>', methods=['GET'])
def profile(user_id):
    if session.get('user_id', "") == "":
        return redirect("/")
    
    if session['user_id'] == int(user_id):
        return render_template("profile.html", pets = db.get_TableDicts(f"SELECT * FROM pets WHERE user_id = '{user_id}';"), user = db.get_TableDicts(f"SELECT * FROM users WHERE user_id = '{user_id}';"))
    
    return redirect("/profile")


@app.route('/petprofile/<user_id>/<pet_id>', methods=['GET'])
def petProfile(user_id, pet_id):
    if session.get('user_id', "") == "":
        return redirect("/")
    if session['user_id'] == int(user_id):
        pet = db.get_TableDicts(f"SELECT * FROM pets WHERE user_id = '{user_id}' AND pet_id = '{pet_id}';")
        user = db.get_TableDicts(f"SELECT * FROM users WHERE user_id = '{user_id}';")
        
        return render_template("petProfile.html", pet=pet, user=user, activities=functions.getPetActivities(user_id, pet_id) )
        
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
    
    db.query(f"INSERT INTO pets (user_id, species, name, gender, birthDate, race) VALUES ('{user_id}', '{request.form['species']}', '{request.form['name']}', '{request.form['gender']}', '{request.form['birthDate']}', '{request.form['race']}')")
    return redirect('/profile')


@app.route('/pet/delete/<user_id>/<pet_id>', methods=['GET'])
def pet_delete(user_id, pet_id):
    if session.get('user_id', "") == "" or int(user_id) != session['user_id']:
        return redirect('/')

    db.query(f"DELETE FROM pets WHERE user_id = '{user_id}' AND pet_id = '{pet_id}';")
    return redirect('/profile')


@app.route('/pet/edit/<user_id>/<pet_id>', methods=['GET', 'POST'])
def pet_edit(user_id, pet_id):
    if session.get('user_id', "") == "" or int(user_id) != session['user_id']:
        return redirect('/')

    if request.method == 'GET':
        return render_template('editPet.html', pet = db.get_TableDicts(f"SELECT * FROM pets WHERE pet_id = '{pet_id}';"))

    db.query(f"UPDATE pets SET species='{request.form['species']}', name='{request.form['name']}', gender='{request.form['gender']}', birthDate='{request.form['birthDate']}', race='{request.form['species']}' WHERE pet_id='{pet_id}'  ")
    return redirect('/profile')


####################


@app.route('/activity/add/<user_id>/<pet_id>', methods=['GET','POST'])
def activity_add(user_id, pet_id):
    if session.get('user_id', "") == "" or int(user_id) != session['user_id']:
        return redirect('/')
    
    if request.method == 'GET':
        return render_template("addActivity.html", user_id = user_id, pet_id = pet_id)
    
    # db.query() I WAS HERE BUT I DONT HAVE A PAGE THAT LEADS TO THIS ACTION
    return str("f")


@app.route('/activity/delete/<user_id>/<activity_id>', methods=['GET'])
def activity_delete(user_id, activity_id):
    if session.get('user_id', "") == "" or int(user_id) != session['user_id']:
        return redirect('/')
    
    db.query(f"DELETE FROM activities WHERE user_id = '{user_id}' AND activity_id = '{activity_id}';")
    return redirect('/profile')


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

@app.route('/api/myUserId')
def myUserId():
    if session.get('user_id', "") == "":
        return ""
    return str(session['user_id'])


@app.route('/api/myActivities')
def myActivities():
    if session.get('user_id', "") == "":
        return ""
    
    activities = []
    functions.updateUserAlerts(session['user_id'])

    for activity in db.get_TableDicts(f"SELECT * FROM activities WHERE user_id = {session['user_id']}"):
        activities.append(activity)
    return activities


@app.route('/api/allUsernames')
def viewUsernames():
    usernames = []
    for user in db.get_TableDicts("SELECT * FROM users"):
        usernames.append(user['username'])
    return usernames


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
    return str(functions.updateUserAlerts('1'))


@app.route('/test2')
def test2():
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


@app.route('/test3')
def test3():
    activities=functions.getPetActivities('2')
    return str(activities)