from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            flag TEXT
        )
    ''')
    # Add dummy and admin users
    cursor.execute("INSERT OR IGNORE INTO users (username, password, flag) VALUES ('user', 'password', NULL)")
    cursor.execute("INSERT OR IGNORE INTO users (username, password, flag) VALUES ('admin', 'supersecret', 'STURSEC{ADVANCED_SQL_INJECTION}')")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template_string('''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Broken Login of Sturtle</title>
    <style>
        /* General Reset */
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-color: #1e1e2f;
            color: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        /* Container */
        .login-container {
            background: #2a2a3c;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            padding: 20px 30px;
            width: 100%;
            max-width: 400px;
            text-align: center;
        }

        /* Title */
        .login-container h1 {
            margin-bottom: 20px;
            font-size: 24px;
            color: #76daff;
        }

        /* Form Styles */
        .login-form label {
            display: block;
            text-align: left;
            margin-bottom: 8px;
            font-size: 14px;
        }

        .login-form input[type="text"],
        .login-form input[type="password"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #555;
            border-radius: 5px;
            background-color: #1e1e2f;
            color: #fff;
            font-size: 14px;
        }

        .login-form input[type="submit"] {
            background-color: #76daff;
            border: none;
            border-radius: 5px;
            padding: 10px 15px;
            color: #000;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.3s ease;
            font-size: 16px;
        }

        .login-form input[type="submit"]:hover {
            background-color: #5cb8e4;
        }

        /* Footer */
        .footer {
            margin-top: 20px;
            font-size: 12px;
            color: #aaa;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>Broken Login of Sturtle</h1>
        <form method="post" action="/login" class="login-form">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>

            <label for="password">Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>

            <input type="submit" value="Login">
        </form>
        <div class="footer">
            <p>Powered by Sturtle Security</p>
        </div>
    </div>
</body>
</html>

    ''')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    # Basic input sanitization
    if "'" in username or "'" in password:
        return "Invalid characters detected."

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Vulnerable SQL query
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        if user[1] == 'admin':
            return f"Welcome, admin! Here is your flag: {user[3]}"
        return f"Welcome, {user[1]}!"
    else:
        return "Invalid credentials. Try again."

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)

