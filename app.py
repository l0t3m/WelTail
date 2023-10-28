#################### Imports: ####################

from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)

import db



#################### Variables: ####################

db.setup()
app.secret_key = "abc_123"



#################### Routes: ####################

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

