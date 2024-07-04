from flask import Flask, render_template, request, redirect, url_for
import string
import secrets
import datetime
import sqlite3

app = Flask(__name__)


def generate_password(length):
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    password = ''.join(secrets.choice(characters) for i in range(length))
    return password


def save_password_to_db(account, password):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS passwords
                 (id INTEGER PRIMARY KEY, timestamp TEXT, account TEXT, password TEXT)''')

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO passwords (timestamp, account, password) VALUES (?, ?, ?)", (timestamp, account, password))
    conn.commit()
    conn.close()


def get_all_passwords():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("SELECT timestamp, account, password FROM passwords")
    passwords = c.fetchall()
    conn.close()
    return passwords


@app.route('/', methods=['GET', 'POST'])
def index():
    password = ""
    if request.method == 'POST':
        try:
            length = int(request.form['length'])
            account = request.form['account'].strip()
            if length < 1 or not account:
                raise ValueError
            password = generate_password(length)
            save_password_to_db(account, password)
        except ValueError:
            password = "Invalid length or account"
    return render_template('index.html', password=password)


@app.route('/view-passwords')
def view_passwords():
    passwords = get_all_passwords()
    return render_template('view_passwords.html', passwords=passwords)


if __name__ == '__main__':
    app.run(debug=True)
