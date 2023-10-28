#################### Imports: ####################

from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)

import db, functions



#################### Variables: ####################

db.setup()
app.secret_key = "abc_123"



#################### Routes: ####################

@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    for user in db.get_TableDicts("SELECT * FROM users"):
        if user['username'] == request.form['username'] and user['password'] == request.form['password']:
            return redirect(f"/feed/{user['user_id']}")

    return render_template("login.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    
    db.query(f"INSERT INTO users (username, password) VALUES ('{request.form['username']}', '{request.form['password']}')")
    return redirect(f"/feed/{functions.getUserData(request.form['username'])['user_id']}")


@app.route('/feed/<user_id>', methods=['GET'])
def feed(user_id):
    return render_template("feed.html")



#################### Test Routes: ####################

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

