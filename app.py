from flask import Flask, render_template, session, request, redirect
from cs50 import SQL
from datetime import timedelta
from helperFunction import login_required, sorry
from werkzeug.security import check_password_hash, generate_password_hash



app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.secret_key = "abcde"
app.permanent_session_lifetime = timedelta(minutes=10)

# Connect to database
db = SQL("sqlite:///playersData.db")


@app.route('/', methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        return render_template("create433.html")
    return render_template("index.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    # reset
    session.clear()

    # User reached route via POST
    if request.method == "POST":

        # Check username
        if not request.form.get("username"):
            return sorry("must provide username", 400)

        # Check password
        if not request.form.get("password"):
            return sorry("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Check username and password
        # result[0][2] is hashed password
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return sorry("invalid username and password", 400)

        # Remember username
        session["user_id"] = rows[0]["id"]

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
            return sorry("must provide username", 400)
        elif not request.form.get("password"):
            return sorry("must provide password", 400)
        elif not request.form.get("confirmation"):
            return sorry("must provide confirmation", 400)

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Check username whether it is available or not
        if len(rows) != 0:
            return sorry("invalid username", 400)

        # Check whether confirmation fits password
        if confirmation != password:
            return sorry("passwords don't match", 400)

        # New registering
        db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", username, generate_password_hash(password))

        # start session
        row = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = row[0]["id"]

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/create433", methods=["GET"])
@login_required
def create():
    if request.method == "GET":
        squad = db.execute("SELECT * FROM players LIMIT 14")
        return render_template("create433.html", squad=squad)


@app.route("/create433", methods=["GET", "POST"])
@login_required
def set_squad():
    if request.method == "POST":
        if request.form.get("symbol1"):
            imagedic = db.execute("SELECT image FROM players WHERE name = ?", request.form.get("symbol1"))
            # この表記重要！DBからとるときは要素が辞書型のリスト型担ってることに注意
            image1 = imagedic[0]['image']
            return render_template("create433.html", image1=image1)
        session.clear()
        return render_template("register.html")

