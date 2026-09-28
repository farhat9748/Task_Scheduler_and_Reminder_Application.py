from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

import mysql.connector
from mysql.connector import Error

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


# ==========================================
# FLASK APPLICATION
# ==========================================

app = Flask(__name__, template_folder="template")

app.secret_key = "taskflow-secret-key-2026"


# ==========================================
# DATABASE CONFIGURATION
# ==========================================

DB_CONFIG = {
    "user": "root",
    "password": "",
    "host": "localhost",
    "port": 3306,
    "database": "task_scheduler"
}


# ==========================================
# DATABASE CONNECTION FUNCTION
# ==========================================

def get_db_connection():

    try:

        connection = mysql.connector.connect(
            **DB_CONFIG
        )

        return connection

    except Error as e:

        print("Database connection error:", e)

        return None


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def index():

    return render_template("index.html")


# ==========================================
# FEATURES PAGE
# ==========================================

@app.route("/features")
def features():

    return render_template("feature.html")


# ==========================================
# HOW IT WORKS PAGE
# ==========================================

@app.route("/how-it-works")
def how_it_works():

    return render_template("how it work.html")


# ==========================================
# LOGIN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password")

        if not email or not password:
            flash("Please enter your email and password.")
            return redirect(url_for("login"))

        connection = get_db_connection()

        if connection is None:
            flash("Database connection failed.")
            return redirect(url_for("login"))

        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                "SELECT id, username, password_hash FROM users WHERE email = %s",
                (email,)
            )
            user = cursor.fetchone()

            if user is None or not check_password_hash(user["password_hash"], password):
                flash("Invalid email or password.")
                return redirect(url_for("login"))

            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Login successful!")
            return redirect(url_for("get_started"))

        except Error as e:
            print("Login error:", e)
            flash("An error occurred during login.")
            return redirect(url_for("login"))

        finally:
            cursor.close()
            connection.close()

    return render_template("login.html")


# ==========================================
# REGISTER
# ==========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Check empty fields

        if not name or not email or not password or not confirm_password:

            flash("Please fill in all fields.")

            return redirect(url_for("register"))

        # Check password match

        if password != confirm_password:

            flash("Passwords do not match.")

            return redirect(url_for("register"))

        # Connect database

        connection = get_db_connection()

        if connection is None:

            flash("Database connection failed.")

            return redirect(url_for("register"))

        cursor = connection.cursor(dictionary=True)

        try:

            # Check existing email

            cursor.execute(
                "SELECT id FROM users WHERE email = %s",
                (email,)
            )

            existing_user = cursor.fetchone()

            if existing_user:

                flash("Email is already registered.")

                return redirect(url_for("register"))

            # Hash password securely

            hashed_password = generate_password_hash(password)

            # Insert user into database

            cursor.execute(
                """
                INSERT INTO users
                (username, email, password_hash)
                VALUES (%s, %s, %s)
                """,
                (name, email, hashed_password)
            )

            connection.commit()

            flash("Account created successfully!")

            return redirect(url_for("login"))

        except Error as e:

            connection.rollback()

            print("Registration error:", e)

            flash("An error occurred during registration.")

            return redirect(url_for("register"))

        finally:

            cursor.close()
            connection.close()

    return render_template("register.html")


# ==========================================
# GET STARTED / DASHBOARD
# ==========================================

@app.route("/get-started")
def get_started():

    if "user_id" not in session:

        flash("Please log in first.")

        return redirect(url_for("login"))

    return render_template("get started.html")


# ==========================================
# EXPLORE FEATURES
# ==========================================

@app.route("/explore-features")
def explore_features():

    return render_template("explore feature.html")


# ==========================================
# CREATE ACCOUNT PAGE
# ==========================================

@app.route("/create-account")
def create_account():

    return render_template("create your free account.html")


# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out.")

    return redirect(url_for("index"))


# ==========================================
# TEST DATABASE CONNECTION
# ==========================================

@app.route("/test-db")
def test_db():

    connection = get_db_connection()

    if connection:

        connection.close()

        return "Database connected successfully!"

    return "Database connection failed."


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )

"""
            <li>
                <a href="{{ url_for('register') }}"
                   class="nav-button">
                    Register
                </a>
            </li>

        </ul>

    </nav>
</header>


<!-- Registration Section -->
<main class="form-container">

    <div class="form-box">

        <!-- Logo -->
        <div class="form-logo">
            Task<span>Flow</span>
        </div>

        <h1>Create Account</h1>

        <p>
            Start organizing your work today.
        </p>


        <!-- Flash Messages -->
        {% with messages = get_flashed_messages() %}

            {% if messages %}

                {% for message in messages %}

                    <div class="message">
                        {{ message }}
                    </div>

                {% endfor %}

            {% endif %}

        {% endwith %}


        <!-- Registration Form -->
        <form method="POST"
              action="{{ url_for('register') }}">

            <!-- Full Name -->
            <div class="form-group">

                <label for="name">
                    Full Name
                </label>

                <input
                    type="text"
                    id="name"
                    name="name"
                    placeholder="Enter your full name"
                    autocomplete="name"
                    required
                >

            </div>


            <!-- Email -->
            <div class="form-group">

                <label for="email">
                    Email Address
                </label>

                <input
                    type="email"
                    id="email"
                    name="email"
                    placeholder="Enter your email"
                    autocomplete="email"
                    required
                >

            </div>


            <!-- Password -->
            <div class="form-group">

                <label for="password">
                    Password
                </label>

                <input
                    type="password"
                    id="password"
                    name="password"
                    placeholder="Create a password"
                    autocomplete="new-password"
                    required
                >

            </div>


            <!-- Confirm Password -->
            <div class="form-group">

                <label for="confirm_password">
                    Confirm Password
                </label>

                <input
                    type="password"
                    id="confirm_password"
                    name="confirm_password"
                    placeholder="Confirm your password"
                    autocomplete="new-password"
                    required
                >

            </div>


            <!-- Submit -->
            <button type="submit"
                    class="btn primary full">
                Create Account
            </button>

        </form>


        <!-- Login Link -->
        <p class="form-bottom">

            Already have an account?

            <a href="{{ url_for('login') }}">
                Login
            </a>

        </p>

    </div>

</main>


<!-- Footer -->
<footer>

    <div class="copyright">
        &copy; 2026 TaskFlow. All Rights Reserved.
    </div>

</footer

</body>

</html>
"""
