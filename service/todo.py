from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

# SQLite database setup
DB_NAME = 'users.db'

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

create_table()

# Helper functions
def get_user_by_username(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def add_user(username, email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
    conn.commit()
    conn.close()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if user already exists
    if get_user_by_username(username):
        return jsonify({'error': 'Username already exists'}), 400

    # Hash password
    hashed_password = generate_password_hash(password)

    # Add user to the database
    add_user(username, email, hashed_password)

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if user exists
    user = get_user_by_username(username)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Check password
    if not check_password_hash(user[3], password):
        return jsonify({'error': 'Invalid password'}), 401

    # Return user data (excluding password)
    user_data = {'id': user[0], 'username': user[1], 'email': user[2]}
    return jsonify(user_data), 200

if __name__ == '__main__':
    app.run(debug=True)