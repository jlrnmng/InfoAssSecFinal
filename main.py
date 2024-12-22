from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
import mysql.connector
from mysql.connector import errorcode
import hashlib
import configparser
import os

# Initialize application
app = Flask(__name__)
app.secret_key = 'admin'  # Session protection

# Upload folder configuration
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# MySQL Connection Management
connection = None

def connect_to_db():
    global connection
    try:
        db_config = read_db_config()
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print('Connected to MySQL Database')
    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Error, Access Denied. Please check your username and password.')
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            print('Error, Database does not Exist.')
        else:
            print(e)

def read_db_config(filename='config.ini', section='mysql'):
    parser = configparser.ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception(f'{section} not found in the {filename} file.')
    return db

# Password hashing functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(hashed_password, password):
    return hashed_password == hashlib.sha256(password.encode()).hexdigest()

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user:
            flash("Username already exists", "danger")
        else:
            cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)", 
                           (username, hashed_password, 'User'))
            connection.commit()
            flash("User registered successfully!", "success")
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user and check_password(user['password_hash'], password):
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['username'] = user['username']  # Store username in session
            flash("Login successful!", "success")
            if user['role'] == "Admin":
                return redirect(url_for("admin_profile"))
            return redirect(url_for("profile"))
        flash("Invalid credentials", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('home'))

@app.route('/admin_profile')
def admin_profile():
    if 'role' not in session or session['role'] != 'Admin':
        abort(403)
    return render_template('users.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        abort(403)

    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'update_info':
            # Update user information
            username = request.form.get('username')
            cursor.execute("UPDATE users SET username = %s WHERE id = %s", (username, session['user_id']))
            connection.commit()
            session['username'] = username  # Update session info
            flash("Profile information updated successfully!", "success")

        elif action == 'change_password':
            # Change password
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')

            # Fetch user's current password hash
            cursor.execute("SELECT password_hash FROM users WHERE id = %s", (session['user_id'],))
            user = cursor.fetchone()
            if user and check_password(user['password_hash'], current_password):
                if new_password == confirm_password:
                    hashed_password = hash_password(new_password)
                    cursor.execute("UPDATE users SET password_hash = %s WHERE id = %s", 
                                   (hashed_password, session['user_id']))
                    connection.commit()
                    flash("Password changed successfully!", "success")
                else:
                    flash("New passwords do not match.", "danger")
            else:
                flash("Current password is incorrect.", "danger")

        elif action == 'update_picture' and 'profile_picture' in request.files:
            # Update profile picture
            picture = request.files['profile_picture']
            if picture.filename != '':
                filename = f"{session['user_id']}_{picture.filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                picture.save(filepath)
                cursor.execute("UPDATE users SET profile_pic = %s WHERE id = %s", (filename, session['user_id']))
                connection.commit()
                flash("Profile picture updated successfully!", "success")

    # Fetch user information for rendering
    cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
    current_user = cursor.fetchone()
    return render_template('profile.html', current_user=current_user)

@app.route('/users', methods=["GET", "POST"])
def users():
    if 'role' not in session or session['role'] != 'Admin':
        abort(403)

    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":
        if 'new_username' in request.form and 'new_password' in request.form and 'new_role' in request.form:
            new_username = request.form['new_username']
            new_password = request.form['new_password']
            new_role = request.form['new_role']

            cursor.execute("SELECT * FROM users WHERE username = %s", (new_username,))
            existing_user = cursor.fetchone()
            if existing_user:
                flash("Username already exists", "danger")
            else:
                hashed_password = hash_password(new_password)
                cursor.execute(
                    "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                    (new_username, hashed_password, new_role),
                )
                connection.commit()
                flash("User registered successfully!", "success")

        elif 'delete_user' in request.form:
            user_id = request.form.get('user_id')
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            connection.commit()
            flash("User deleted successfully", "success")

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template('users.html', users=users)

if __name__ == '__main__':
    connect_to_db()
    app.run(debug=True)
