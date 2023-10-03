from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helper import apology

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# main reguest
@app.route("/")
def landing():
    return render_template("landing.html")

# register coach function
@app.route("/registercoach.html", methods=["GET", "POST"])
def registercoach():
    """Register user"""
    if request.method == "GET":
        return render_template("registercoach.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("Must Give Username")

        if not password:
            return apology("Must Give Password")

        # Check if the username already exists
        existing_user = db.execute("SELECT id FROM coaches WHERE username = ?", username)

        if existing_user:
            return apology("Username already exists")

        hash = generate_password_hash(password)

        try:
            new_user = db.execute("INSERT INTO coaches(username,hash) VALUES(?,?)", username, hash)

        except:
            return apology("Username already exists")

        session["user_id"] = new_user

        return redirect("/")

# register athlete function
@app.route("/registerathlete.html", methods=["GET", "POST"])
def registerathlete():
    """Register user"""
    if request.method == "GET":
        return render_template("registerathlete.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("Must Give Username")

        if not password:
            return apology("Must Give Password")

        # Check if the username already exists
        existing_user = db.execute("SELECT id FROM athletes WHERE username = ?", username)

        if existing_user:
            return apology("Username already exists")

        hash = generate_password_hash(password)

        coachUsername = session["coachUsername"]

        try:
            new_user = db.execute("INSERT INTO athletes(username,hash, coach) VALUES(?,?,?)", username, hash, coachUsername)

        except:
            return apology("Username already exists")

        try:
            db.execute("INSERT INTO profile VALUES(?,?,?,?,?,?,?,?)", username, '', 0, '', '', '', '', '')

        except:
            return apology("Error")

        session["user_id"] = new_user

        # Fetch athlete usernames for the coach landing page
        athlete_usernames = db.execute("SELECT username FROM athletes WHERE coach = ?", coachUsername)

        # Redirect user to coach landing page with athlete usernames
        return render_template('coachlanding.html', coachusername=coachUsername, athlete_usernames=athlete_usernames)

# coach login function
@app.route("/logincoach.html", methods=["GET", "POST"])
def coachlogin():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "GET":
        return render_template("logincoach.html")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM coaches WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Pass the username to the coachlanding.html template
        coach_username = rows[0]["username"]
        session["coachUsername"] = coach_username

        athlete_usernames = db.execute("SELECT username FROM athletes WHERE coach = ?", coach_username)

        return render_template('coachlanding.html', coachusername=coach_username, athlete_usernames=athlete_usernames)

# athlete login function
@app.route("/loginathlete.html", methods=["GET", "POST"])
def athletelogin():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "GET":
        return render_template("loginathlete.html")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM athletes WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        username = rows[0]["username"]

        try:
            # Execute the SQL query to fetch athlete profile information
            profile_data = db.execute("SELECT fullname, user_id, date_of_birth, school, age_group, coach, two_km, one_km FROM profile WHERE fullname = ?", username)

            if len(profile_data) == 1:
                # Extract profile information from the result
                profile = profile_data[0]
                fullname = profile["fullname"]
                user_id = profile["user_id"]
                date_of_birth = profile["date_of_birth"]
                school = profile["school"]
                age_group = profile["age_group"]
                coach = profile["coach"]
                two_km = profile["two_km"]
                one_km = profile["one_km"]

            else:
                return apology("Profile not found for the given username", 404)

        except:
            return apology("An error occurred while fetching profile")

        # Redirect user to home page with profile information
        return render_template("athletelanding.html", username=username, fullname=fullname, user_id=user_id, date_of_birth=date_of_birth, school=school, age_group=age_group, coach=coach, two_km=two_km, one_km=one_km)



@app.route("/logout.html")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route('/editathleteform.html', methods=["GET","POST"])
def editathleteform():

    if request.method == "GET":
        return render_template('editathleteform.html')

    if request.method == "POST":
        username = request.form.get("fullname")
        user_id = request.form.get("id")
        date_of_birth = request.form.get("date_of_birth")
        school = request.form.get("school")
        age_group = request.form.get("age_group")
        coach = request.form.get("coach")
        two_km = request.form.get("two_km")
        one_km = request.form.get("one_km")

        if not username:
            return apology("Must Give a Fullname")

        if not user_id:
            return apology("Must Give an ID")

        if not date_of_birth:
            return apology("Must Give a Date of Birth")

        if not school:
            return apology("Must Give a School")

        if not age_group:
            return apology("Must Give a Age Group")

        if not coach:
            return apology("Must Give a Coach")

        if not two_km:
            return apology("Must Give a 2km PB")

        if not one_km:
            return apology("Must Give a 1km PB")

        coachUsername = session["coachUsername"]

        try:
            db.execute("UPDATE profile SET user_id=?, date_of_birth=?, school=?, age_group=?, coach=?, two_km=?, one_km=? WHERE fullname=?", user_id, date_of_birth, school, age_group, coach, two_km, one_km, username)

        except:
            return apology("Error")

        # Fetch athlete usernames for the coach landing page
        athlete_usernames = db.execute("SELECT username FROM athletes WHERE coach = ?", coachUsername)

        # Redirect user to coach landing page with athlete usernames
        return render_template('coachlanding.html', coachusername=coachUsername, athlete_usernames=athlete_usernames)

# athlete login function
@app.route("/contact.html", methods=["GET"])
def contact():

    if request.method == "GET":
        return render_template("contact.html")

# athlete login function
@app.route("/athletelanding", methods=["GET"])
def athletelanding():

    if request.method == "GET":

        username = request.args.get('username')

        try:
            # Execute the SQL query to fetch athlete profile information
            profile_data = db.execute("SELECT fullname, user_id, date_of_birth, school, age_group, coach, two_km, one_km FROM profile WHERE fullname = ?", username)

            if len(profile_data) == 1:
                # Extract profile information from the result
                profile = profile_data[0]
                fullname = profile["fullname"]
                user_id = profile["user_id"]
                date_of_birth = profile["date_of_birth"]
                school = profile["school"]
                age_group = profile["age_group"]
                coach = profile["coach"]
                two_km = profile["two_km"]
                one_km = profile["one_km"]

            else:
                return apology("Profile not found for the given username", 404)

        except:
            return apology("An error occurred while fetching profile")

        # Redirect user to home page with profile information
        return render_template("athletelanding.html", username=username, fullname=fullname, user_id=user_id, date_of_birth=date_of_birth, school=school, age_group=age_group, coach=coach, two_km=two_km, one_km=one_km)

