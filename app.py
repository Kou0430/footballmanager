from flask import Flask, render_template, session, request, redirect
from datetime import timedelta
from helpers import login_required, apology
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.secret_key = "abcde"
app.permanent_session_lifetime = timedelta(minutes=10)

# Connect to database
conn = sqlite3.connect('playersData.db')
cur = conn.cursor()


@app.route('/')
@login_required
def index():
    return render_template("index.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    # reset
    session.clear()

    # User reached route via POST
    if request.method == "POST":

        # Check username
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Check password
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        cur.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        result = cur.fetchall()
        # Check username and password
        if len(result) != 1 or not check_password_hash(result[0][2], request.form.get("password")):  # result[0][2] is hashed password
            return apology("invalid username and password", 403)

        # Remember username
        session["user_id"] = result[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():

    # Forget user information
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():

    session.clear()

    # User reached route via POST
    if request.method == "POST":

        # Ensure submit
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Query database for username
        cur.execute("SELECT * FROM users WHERE username = ?", username)
        result = cur.fetchall()

        # Check username whether it is available or not
        if len(result) != 0:
            return apology("invalid username", 400)

        # Check whether confirmation fits password
        if confirmation != password:
            return apology("passwords don't match", 400)

        # New registering
        cur.execute("INSERT INTO users(username, hash) VALUES(?, ?)", (username, generate_password_hash(password)))
        conn.commit()

        # start session
        cur.execute("SELECT * FROM users WHERE username = ?", username)
        result = cur.fetchall()
        session["user_id"] = result[0][0]

        redirect("/")

    else:
        return render_template("register.html")




conn.close()
