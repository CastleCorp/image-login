from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
import sqlite3

app = Flask(__name__)
app.secret_key = b'<Your Secret Key>'
# Initialize the SQLite database
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        fingerprint TEXT
    )
''')
conn.commit()

@app.route('/')
def index():
    if 'username' in session:
        login_string = f"Currently logged in as {session.get('username')}"
    else:
        login_string = "Not currently logged in"
    return render_template('index.html', is_logged_in=login_string)

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['image_data']

    # Hash the image data
    image_hash = hashlib.sha256(password.encode()).hexdigest()

    # Store username and hashed image data in the database
    cursor.execute('''
        INSERT INTO users (username, password)
        VALUES (?, ?)
    ''', (username, image_hash))
    conn.commit()

    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['image_data']

    # Hash the image data for comparison
    image_hash = hashlib.sha256(password.encode()).hexdigest()

    # Retrieve user data from the database
    cursor.execute('''
        SELECT * FROM users WHERE username=?
    ''', (username,))
    user = cursor.fetchone()

    # Check if the user exists and if the image hash matches
    if user and user[2] == image_hash:  # Index 2 corresponds to the password column
        session['username'] = username
        return "Login successful! <br><button><a href=\"/\">Go home</a></button>"
    else:
        return "Login failed! <br><button><a href=\"/\">Go home</a></button>"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
