from flask import Flask, request, render_template, jsonify, redirect, url_for, session  # Updated imports
import numpy as np
import pandas as pd
import pickle
import sqlite3
import hashlib

# flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# load databasedataset===================================
sym_des = pd.read_csv("dataset/symtoms_df.csv")
precautions = pd.read_csv("dataset/precautions_df.csv")
workout = pd.read_csv("dataset/workout_df.csv")
description = pd.read_csv("dataset/description.csv")
medications = pd.read_csv('dataset/medications.csv')
diets = pd.read_csv("dataset/diets.csv")

# load model===========================================
svc = pickle.load(open('model/svc.pkl','rb'))

#============================================================
# custome and helping functions
#==========================helper funtions================
def helper(dis):
    desc = description[description['Disease'] == dis]['Description']
    desc = " ".join([w for w in desc])

    pre = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = [col for col in pre.values]

    med = medications[medications['Disease'] == dis]['Medication']
    med = [med for med in med.values]

    die = diets[diets['Disease'] == dis]['Diet']
    die = [die for die in die.values]

    wrkout = workout[workout['disease'] == dis] ['workout']

    return desc, pre, med, die, wrkout

# User authentication routes
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Hash the password
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Username already exists!"
        finally:
            conn.close()
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Hash the password
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        user = cursor.fetchone()
        if user:
            session['username'] = username
            return redirect(url_for('home'))  # Redirect to the home page
        return "Invalid username or password!"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Redirect root to login
@app.route("/")
def index():
    return redirect(url_for('login'))

# Define a route for the home page
@app.route('/predict', methods=['GET', 'POST'])
def home():
    if 'username' not in session:  # Check if user is logged in
        return redirect(url_for('login'))  # Redirect to login if not authenticated

    if request.method == 'POST':
        symptoms = request.form.get('symptoms')
        print(symptoms)
        if symptoms == "Symptoms":
            message = "Please either write symptoms or you have written misspelled symptoms"
            return render_template('index.html', message=message)
        else:
            user_symptoms = [s.strip() for s in symptoms.split(',')]
            user_symptoms = [symptom.strip("[]' ") for symptom in user_symptoms]
            predicted_disease = get_predicted_value(user_symptoms)
            dis_des, precautions, medications, rec_diet, workout = helper(predicted_disease)

            my_precautions = []
            for i in precautions[0]:
                my_precautions.append(i)

            return render_template('index.html', predicted_disease=predicted_disease, dis_des=dis_des,
                                   my_precautions=my_precautions, medications=medications, my_diet=rec_diet,
                                   workout=workout)

    return render_template('index.html')

# about view function and path
@app.route('/about')
def about():
    return render_template("about.html")

# contact view function and path
@app.route('/contact')
def contact():
    return render_template("contact.html")

# developer view function and path
@app.route('/developer')
def developer():
    return render_template("developer.html")

# blog view function and path
@app.route('/blog')
def blog():
    return render_template("blog.html")

if __name__ == '__main__':
    app.run(debug=True)
