from flask import Flask, render_template, session, request, redirect
from cs50 import SQL
from datetime import timedelta
from helperFunction import login_required, sorry, calculate433
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.secret_key = "abcde"
app.permanent_session_lifetime = timedelta(minutes=10)

# Connect to database
db = SQL("sqlite:///playersData.db")

squadlist = [''] * 20  # １１人なので１１にしようとしたらout of rangeでた、なぜ


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


# create433------------------------------
@app.route("/create433", methods=["GET"])
@login_required
def create433():
    if request.method == "GET":
        for i in range(20):
            squadlist[i] = ""

        squad = db.execute("SELECT * FROM players LIMIT 40")  # ！！！！ここは後で改善

        check = db.execute("SELECT * FROM squads WHERE username = ?", session["user_id"])
        if len(check) == 0:
            for i in range(40):
                db.execute("INSERT INTO squads(username, name) VALUES(?, ?)", session["user_id"], squad[i]["name"])
        return render_template("create433.html", squad=squad)


@app.route("/create433", methods=["GET", "POST"])
@login_required
def set_squad433():
    if request.method == "POST":
        mysquad = db.execute("SELECT * FROM squads WHERE username = ?", session["user_id"])
        for i in range(20):  # 11人なので11にしようと思ったらなぜかout of rangeでたので多めにしてる
            if request.form.get("symbol{num}".format(num=i)):
                imagedict = db.execute("SELECT name, image FROM players WHERE name = ?",
                                       request.form.get("symbol{num}".format(num=i)))
                squadlist[i-1] = imagedict[0]['image']

        current_squad = []

        if squadlist.count('') == 9:  # squadlistは長さ20にしてるので、9個空白が残れば11人入ってる
            for i in range(11):
                squad_temp = db.execute("SELECT * FROM players WHERE image = ?", squadlist[i])
                current_squad.append(squad_temp[0])
        print(current_squad)
        if len(current_squad) != 11:  # 未入力の場合戻る
            return render_template("create433.html", squad=mysquad, image1=squadlist[0], image2=squadlist[1],
                                   image3=squadlist[2], image4=squadlist[3], image5=squadlist[4], image6=squadlist[5],
                                   image7=squadlist[6], image8=squadlist[7], image9=squadlist[8], image10=squadlist[9],
                                   image11=squadlist[10])
        idList = []
        for i in range(11):
            getId = current_squad[i]["id"]
            idList.append(getId)

        if len(idList) != len(set(idList)):  # 重複があればやり直し
            return render_template("create433.html", squad=mysquad, image1=squadlist[0], image2=squadlist[1],
                                   image3=squadlist[2], image4=squadlist[3], image5=squadlist[4], image6=squadlist[5],
                                   image7=squadlist[6], image8=squadlist[7], image9=squadlist[8], image10=squadlist[9],
                                   image11=squadlist[10], message="There is a duplicate!")
        else:
            add = calculate433(current_squad)
            total = add
            for i in range(len(current_squad)):  # スコア計算
                oa = current_squad[i]["oa"]
                pt = current_squad[i]["pt"]
                total += int((oa + pt) / 2)

            return render_template("create433.html", squad=mysquad, image1=squadlist[0], image2=squadlist[1],
                                   image3=squadlist[2], image4=squadlist[3], image5=squadlist[4], image6=squadlist[5],
                                   image7=squadlist[6], image8=squadlist[7], image9=squadlist[8], image10=squadlist[9],
                                   image11=squadlist[10], total=total, add=add)

    return render_template("register.html")


# create442------------------------------------
@app.route("/create442", methods=["GET"])
@login_required
def create442():
    if request.method == "GET":
        squad = db.execute("SELECT * FROM players LIMIT 40")  # ！！！！ここは後で改善
        check = db.execute("SELECT * FROM squads WHERE username = ?", session["user_id"])
        if len(check) == 0:
            for i in range(40):
                db.execute("INSERT INTO squads(username, name) VALUES(?, ?)", session["user_id"], squad[i]["name"])
        return render_template("create442.html", squad=squad)


@app.route("/create442", methods=["GET", "POST"])
@login_required
def set_squad442():
    if request.method == "POST":

        mysquad = db.execute("SELECT * FROM squads WHERE username = ?", session["user_id"])
        for i in range(20):  # 11人なので11にしようと思ったらなぜかout of rangeでたので多めにしてる
            if request.form.get("symbol{num}".format(num=i)):
                imagedict = db.execute("SELECT image FROM players WHERE name = ?",
                                       request.form.get("symbol{num}".format(num=i)))
                squadlist[i-1] = imagedict[0]['image']

        return render_template("create442.html", squad=mysquad, image1=squadlist[0], image2=squadlist[1],
                               image3=squadlist[2], image4=squadlist[3], image5=squadlist[4], image6=squadlist[5],
                               image7=squadlist[6], image8=squadlist[7], image9=squadlist[8], image10=squadlist[9],
                               image11=squadlist[10])

    return render_template("register.html")


# create352------------------------------
@app.route("/create352", methods=["GET"])
@login_required
def create352():
    if request.method == "GET":
        squad = db.execute("SELECT * FROM players LIMIT 40")  # ！！！！ここは後で改善
        check = db.execute("SELECT * FROM squads WHERE username = ?", session["user_id"])
        if len(check) == 0:
            for i in range(40):
                db.execute("INSERT INTO squads(username, name) VALUES(?, ?)", session["user_id"], squad[i]["name"])
        return render_template("create352.html", squad=squad)


@app.route("/create352", methods=["GET", "POST"])
@login_required
def set_squad352():
    if request.method == "POST":

        mysquad = db.execute("SELECT * FROM squads WHERE username = ?", session["user_id"])
        for i in range(20):  # 11人なので11にしようと思ったらなぜかout of rangeでたので多めにしてる
            if request.form.get("symbol{num}".format(num=i)):
                imagedict = db.execute("SELECT image FROM players WHERE name = ?",
                                       request.form.get("symbol{num}".format(num=i)))
                squadlist[i-1] = imagedict[0]['image']

        return render_template("create352.html", squad=mysquad, image1=squadlist[0], image2=squadlist[1],
                               image3=squadlist[2], image4=squadlist[3], image5=squadlist[4], image6=squadlist[5],
                               image7=squadlist[6], image8=squadlist[7], image9=squadlist[8], image10=squadlist[9],
                               image11=squadlist[10])

    return render_template("register.html")
