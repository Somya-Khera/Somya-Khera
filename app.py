from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
import mysql.connector
from mysql.connector import IntegrityError, Error
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

# Function to get a new database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except Error as err:
        print(f"Database connection error: {err}")
        return None

# Function to execute a query with error handling
def execute_query(query, params=None, fetch=False):
    connection = get_db_connection()
    if not connection:
        return None, "Database connection failed"
    
    try:
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
        else:
            connection.commit()
            result = cursor.lastrowid
        cursor.close()
        connection.close()
        return result, None
    except Error as err:
        print(f"Query execution error: {err}")
        connection.close()
        return None, str(err)

# Create tables if they don't exist
def create_tables():
    queries = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS career_fields (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            course_required VARCHAR(100),
            skills_required TEXT,
            related_jobs TEXT,
            description TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS search_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            query VARCHAR(255) NOT NULL,
            searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    ]
    
    for query in queries:
        _, error = execute_query(query)
        if error:
            print(f"Error creating table: {error}")

def insert_sample_careers():
    sample_careers = [
        {
            "name": "Software Engineer",
            "course_required": "Computer Science, Software Engineering",
            "skills_required": "Programming, Problem Solving, Algorithms, Data Structures",
            "related_jobs": "Full Stack Developer, Backend Developer, Frontend Developer",
            "description": "Software engineers design, develop, and maintain software applications. They work with various programming languages and frameworks to create efficient and scalable solutions."
        },
        {
            "name": "Data Scientist",
            "course_required": "Data Science, Statistics, Computer Science",
            "skills_required": "Python, R, Machine Learning, Data Analysis, Statistics",
            "related_jobs": "Data Analyst, Machine Learning Engineer, Business Intelligence Analyst",
            "description": "Data scientists analyze complex data sets to extract insights and build predictive models. They use statistical methods and machine learning algorithms to solve business problems."
        },
        {
            "name": "Web Developer",
            "course_required": "Web Development, Computer Science",
            "skills_required": "HTML, CSS, JavaScript, React, Node.js",
            "related_jobs": "Frontend Developer, Full Stack Developer, UI/UX Developer",
            "description": "Web developers create and maintain websites and web applications. They work with various technologies to build responsive and user-friendly interfaces."
        },
        {
            "name": "Cybersecurity Analyst",
            "course_required": "Cybersecurity, Computer Science",
            "skills_required": "Network Security, Ethical Hacking, Risk Assessment, Security Tools",
            "related_jobs": "Information Security Analyst, Security Engineer, Penetration Tester",
            "description": "Cybersecurity analysts protect computer systems and networks from cyber threats. They monitor systems for security breaches and implement security measures."
        }
    ]

    for career in sample_careers:
        result, error = execute_query(
            "INSERT IGNORE INTO career_fields (name, course_required, skills_required, related_jobs, description) VALUES (%s, %s, %s, %s, %s)",
            (career["name"], career["course_required"], career["skills_required"], career["related_jobs"], career["description"])
        )
        if error:
            print(f"Error inserting sample career {career['name']}: {error}")

# Initialize tables and sample data
create_tables()
insert_sample_careers()

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

        result, error = execute_query(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, password)
        )

        if error:
            if "Duplicate entry" in error:
                flash("Email already exists. Please use a different email.")
            else:
                flash(f"Error during signup: {error}")
            return redirect(url_for("signup"))

        session["user_id"] = result
        return redirect(url_for("career_search"))

    return render_template("signup.html")

# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = escape(request.form["email"])
        password = request.form["password"]

        result, error = execute_query(
            "SELECT * FROM users WHERE email = %s",
            (email,),
            fetch=True
        )

        if error:
            flash(f"Error during login: {error}")
            return redirect(url_for("login"))

        if result and check_password_hash(result[0][3], password):
            session["user_id"] = result[0][0]
            return redirect(url_for("career_search"))

        flash("Invalid email or password.")
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

    # Store search history
    _, error = execute_query(
        "INSERT INTO search_history (user_id, query) VALUES (%s, %s)",
        (session["user_id"], query)
    )
    if error:
        print(f"Error storing search history: {error}")

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
    results, error = execute_query(sql_query, values, fetch=True)

    if error:
        return {"error": f"Search error: {error}"}, 500

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

# Run App
if __name__ == "__main__":
    app.run(debug=True)
