import sqlite3

def check_users_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Check if the users table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone() is not None
    
    conn.close()
    return table_exists

if _name_ == "_main_":
    if check_users_table():
        print("The 'users' table exists.")
    else:
        print("The 'users' table does not exist.")