#################### Imports: ####################

from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)

import db, functions



#################### Variables: ####################

db.setup(filename="weltail.db", testData=True)
app.secret_key = "_WelTail_"



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
    db.query(f"INSERT INTO users (username, fullname, password) VALUES ('{request.form['username']}','{request.form['fullname']}', '{request.form['password']}');")
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
        return render_template("profile.html", user=db.get_TableDicts(f"SELECT * FROM users WHERE user_id = {session['user_id']}")[0], pets = db.get_TableDicts(f"SELECT * FROM pets WHERE user_id = '{user_id}';"))
    return redirect("/profile")


@app.route('/petprofile/<user_id>/<pet_id>', methods=['GET'])
def petProfile(user_id, pet_id):
    if session.get('user_id', "") == "":
        return redirect("/")
    if session['user_id'] == int(user_id):
        activities=functions.reformat_activities(functions.getPetActivities(user_id, pet_id))
        return render_template("petProfile.html", user_id=user_id, pet=db.get_TableDicts(f"SELECT * FROM pets WHERE user_id = '{user_id}' AND pet_id = '{pet_id}';"), activities = 0 if len(activities) == 0 else activities)
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
    
    db.query(f"INSERT INTO pets (user_id, species, name, gender, birthDate, race) VALUES ('{user_id}', '{request.form['species']}', '{request.form['name'].capitalize()}', '{request.form['gender']}', '{request.form['birthDate']}', '{request.form['race'].capitalize()}');")
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

    if request.form['repeat'] == "on":
        newData = functions.reformat_activity(request.form['nextAlert'], request.form['repeat'], request.form['repeatType'], request.form['repeatAmount'])
        db.query(f"INSERT INTO activities (user_id, pet_id, type, name, repeat, nextAlert, repeatInterval) VALUES ({user_id}, {pet_id}, '{request.form['type']}', '{request.form['name'].capitalize()}', {newData[0]}, '{newData[1]}', '{newData[2]}');")
    else:
        newData = functions.reformat_activity(request.form['nextAlert'], request.form['repeat'], request.form['repeatType'], request.form['repeatAmount'])
        db.query(f"INSERT INTO activities (user_id, pet_id, type, name, repeat, nextAlert, repeatInterval) VALUES ({user_id}, {pet_id}, '{request.form['type']}', '{request.form['name'].capitalize()}', {newData[0]}, '{newData[1]}', '{newData[2]}');")
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

    newData = functions.reformat_activity(request.form['nextAlert'], request.form['repeat'], request.form['repeatType'], request.form['repeatAmount'])
    db.query(f"UPDATE activities SET type='{request.form['type'].capitalize()}', name='{request.form['name'].capitalize()}', repeat='{newData[0]}', nextAlert='{newData[1]}', repeatInterval={newData[2]} WHERE activity_id = {session['activity']['activity_id']};")
    session.pop('activity', default=None)
    return redirect("/feed")



#################### Redirect Routes: ####################

@app.route('/feed', methods=['GET'])
def redirect_feed():
    if session.get('user_id', "") == "":
        return redirect("/")
    return redirect(f"/feed/{session['user_id']}")


@app.route('/profile', methods=['GET'])
def redirect_profile():
    if session.get('user_id', "") == "":
        return redirect("/")
    return redirect(f"/profile/{session['user_id']}")



#################### API Routes: ####################

@app.route('/api/myUser', methods=['GET'])
def myUser():
    if session.get('user_id', "") == "":
        return ""
    return db.get_TableDicts(f"SELECT * FROM users WHERE user_id = {session['user_id']}")[0]


@app.route('/api/myPets', methods=['GET'])
def myPets():
    if session.get('user_id', "") == "":
        return ""
    return db.get_TableDicts(f"SELECT * FROM pets WHERE user_id = {session['user_id']}")


@app.route('/api/myActivities', methods=['GET'])
def myActivities():
    if session.get('user_id', "") == "":
        return ""
    return functions.reformat_activities(db.get_TableDicts(f"SELECT * FROM activities WHERE user_id = {session['user_id']} ORDER BY nextAlert;"))


@app.route('/api/myUpcomingActivities', methods=['GET'])
def myUpcomingActivities():
    if session.get('user_id', "") == "":
        return ""
    return functions.reformat_activities(functions.getUpcomingAlerts(session['user_id']))


@app.route('/api/getTargetedActivity', methods=['GET'])
def getTargetedActivity():
    '''Returns the last activity targeted. Used in Edit Activity.'''
    if session.get('user_id', "") == "":
        return ""
    try:
        return session['activity']
    except:
        return []


@app.route('/api/allUsernames', methods=['GET'])
def viewUsernames():
    usernames = []
    for user in db.get_TableDicts("SELECT * FROM users"):
        usernames.append(user['username'])
    return usernames


@app.route('/api/greetingMessage', methods=['GET'])
def greetingMessage():
    '''Returns a greeting message according to the current time.'''
    return functions.generate_greetingMessage()
