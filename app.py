from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
import mysql.connector
from mysql.connector import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import escape
import os
import atexit

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', "this will work!!")  # Replace in production

# Database credentials
DB_HOST = "sql12.freesqldatabase.com"
DB_USER = "sql12771575"
DB_PASSWORD = "SWC73NZGtV"  # Replace with your actual password
DB_NAME = "sql12771575"


# Function to connect to the database
def connect_to_db():
    try:
        db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return db
    except mysql.connector.Error as err:
        print(f"Remote DB connection error: {err}")
        return None

# Initialize database connection
db = connect_to_db()
if db:
    cursor = db.cursor()
else:
    cursor = None
    exit(1)

# Close the database connection when the application exits
def close_db():
    if cursor:
        cursor.close()
    if db:
        db.close()

atexit.register(close_db)

# Create tables if they don't exist
try:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS career_fields (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            course_required VARCHAR(100),
            skills_required TEXT,
            related_jobs TEXT,
            description TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            query VARCHAR(255) NOT NULL,
            searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    db.commit()
except mysql.connector.Error as err:
    print(f"Error creating tables: {err}")

# Home Route
@app.route("/")
def home():
    return redirect(url_for("login"))

# Signup Route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = escape(request.form["username"])
        email = escape(request.form["email"])
        password = generate_password_hash(request.form["password"], method="pbkdf2:sha256")

        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                           (username, email, password))
            db.commit()
            session["user_id"] = cursor.lastrowid
            return redirect(url_for("career_search"))
        except IntegrityError:
            flash("Email already exists.")
        except mysql.connector.Error as err:
            print(f"Database error during signup: {err}")
            flash("Database error occurred.")
        return redirect(url_for("signup"))

    return render_template("signup.html")

# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = escape(request.form["email"])
        password = request.form["password"]

        try:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user and check_password_hash(user[3], password):
                session["user_id"] = user[0]
                return redirect(url_for("career_search"))

            flash("Invalid credentials.")
        except mysql.connector.Error as err:
            print(f"Database error during login: {err}")
            flash("Database error occurred.")
        return redirect(url_for("login"))

    return render_template("login.html")

# Logout Route
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))

# Career Search Page Route
@app.route("/career_search")
def career_search():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("career_search.html")

# Search Route
@app.route("/search", methods=["GET"])
def search():
    if "user_id" not in session:
        return {"error": "Not logged in"}, 401

    query = request.args.get("q", "").strip()
    if not query:
        return {"error": "No query provided"}, 400

    try:
        # Store search history
        cursor.execute("INSERT INTO search_history (user_id, query) VALUES (%s, %s)", (session["user_id"], query))
        db.commit()

        # Search in career_fields table
        sql_query = """
            SELECT name, course_required, skills_required, related_jobs, description
            FROM career_fields
            WHERE name LIKE %s
               OR course_required LIKE %s
               OR skills_required LIKE %s
               OR related_jobs LIKE %s
               OR description LIKE %s
        """
        values = (f"%{query}%",) * 5
        cursor.execute(sql_query, values)
        results = cursor.fetchall()

        if results:
            careers = [{
                "name": row[0],
                "course_required": row[1],
                "skills_required": row[2],
                "related_jobs": row[3],
                "description": row[4]
            } for row in results]
            return {"results": careers}

        return {"message": "No matching careers found"}

    except mysql.connector.Error as err:
        print(f"Database error during search: {err}")
        return {"error": "Database error"}, 500

# Run App
if __name__ == "__main__":
    app.run(debug=True)
