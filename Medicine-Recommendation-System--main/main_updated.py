from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import numpy as np
import pandas as pd
import pickle

# Database connection functions
def create_connection():
    """Create a database connection to the SQLite database."""
    conn = sqlite3.connect('users.db')
    return conn

def create_user(username, password):
    """Create a new user in the users table."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, generate_password_hash(password)))
    conn.commit()
    conn.close()

def get_user(username):
    """Retrieve a user by username."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Load dataset
sym_des = pd.read_csv("dataset/symtoms_df.csv")
precautions = pd.read_csv("dataset/precautions_df.csv")
workout = pd.read_csv("dataset/workout_df.csv")
description = pd.read_csv("dataset/description.csv")
medications = pd.read_csv('dataset/medications.csv')
diets = pd.read_csv("dataset/diets.csv")

# Load model
svc = pickle.load(open('model/svc.pkl','rb'))

# Helper functions
def helper(dis):
    desc = description[description['Disease'] == dis]['Description']
    desc = " ".join([w for w in desc])

    pre = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = [col for col in pre.values]

    med = medications[medications['Disease'] == dis]['Medication']
    med = [med for med in med.values]

    die = diets[diets['Disease'] == dis]['Diet']
    die = [die for die in die.values]

    wrkout = workout[workout['disease'] == dis]['workout']

    return desc, pre, med, die, wrkout

# Routes
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        create_user(username, password)
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]  # Store user ID in session
            return redirect(url_for('index'))  # Redirect to a protected page
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('index.html')

# Other routes...
@app.route('/predict', methods=['GET', 'POST'])
def home():
    # Existing prediction logic...
    pass

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/developer')
def developer():
    return render_template("developer.html")

@app.route('/blog')
def blog():
    return render_template("blog.html")

if __name__ == '__main__':
    app.run(debug=True)
