from flask import Flask, request, render_template, redirect, url_for
app = Flask(_name_)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        print("Received signup request")  # Log the request
        username = request.form['username']
        print(f"Username: {username}")  # Log received username
        password = request.form['password']
        
        print("Establishing database connection...")  # Log connection attempt
        conn = get_db_connection()
        try:
            print("Inserting user into database...")  # Log insertion attempt
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            print("User inserted successfully")  # Log successful insertion
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            print("Username already exists. Please choose a different one.")  # Log existing username error
            return "Username already exists. Please choose a different one."
        finally:
            conn.close()
            print("Database connection closed.")  # Log connection closure

    print("Rendering signup page.")  # Log rendering of the signup page
    return render_template('signup.html')

if _name_ == '_main_':
    app.run(debug=True)