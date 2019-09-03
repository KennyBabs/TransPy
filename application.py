from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request,url_for,session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

#configure application
app = Flask(__name__)

#Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

#Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["cache-control"] = "no-cache, no-store, must-validate"
    response.headers["expires"] = 0
    response.headers["pragma"] = "no-cache"
    return response

#Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#configure cs50 Library to use SQLite database
db = SQL("sqlite:///transpy.db")

@app.route("/")
@login_required #this needs to be implemented on helpers.py
def index():
    # return apology("you need to work on the booking page", 400)
    return render_template("booking.html")

@app.route("/login", methods=["GET","POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure email was submitted
        if not request.form.get("email"):
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for email
        rows = db.execute("SELECT * FROM users WHERE email = :email",
                          email=request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


#listening for the register route
@app.route("/register", methods=["GET","POST"])
def register():
    #check if the route was entered via POST
    if request.method == "POST":
        #check if all fields were properly filled 
        if not request.form.get("firstname"):
            return apology("you omitted your firstname", 400) #note, this is yet to be implemented
        elif not request.form.get("lastname"):
            return apology("you omitted your lastname", 400)
        elif not request.form.get("email"):
            return apology("you omitted your email", 400)
        elif not request.form.get("phone"):
            return apology("you omitted your phone number", 400)
        elif not request.form.get("password"):
            return apology("you must enter a password", 400)
        elif not request.form.get("password") == request.form.get("confirmation"): #check what was used for the input name
            return apology("passwords do not match", 400)
        # generate a hash for the password
        hash = generate_password_hash(request.form.get("password"))
        #insert the form values into the database
        new_user = db.execute("INSERT INTO users (phone, firstname, lastname, email, hash) VALUES (:phone, :firstname, :lastname, :email, :hash)", phone=request.form.get("phone"), firstname=request.form.get("firstname"), lastname=request.form.get("lastname"), email=request.form.get("email"), hash=hash)
        #checks if username has been taken
        if not new_user:
           return apology("username taken", 400) # ensure you update this in apology.html
        else:
            flash("Registered") #ensure that this was implemenmted in layout.html
            #remembers the newly registered user so he can be immediately logged in
            session["user_id"] = new_user
            #redirects user to the landing page immediately the info is inserted properly
            return redirect(url_for("index"))
    #if user entered route via GET method, render register.html
    elif request.method == "GET":
        return render_template("registration.html") 

#recall to setup the database as required
@app.route("/booking")
def booking():
    terminal = request.form.get("terminal") 
    date = request.form.get("date")
    db.execute("INSERT INTO transactions (terminal, date) VALUES (:terminal, :date)", terminal=terminal, date=date)
    
@app.route("/seatselect")
def seatselect():
    arr = []
    seat = request.args.get("seat") #ensure that this name was used in the booking page
    arr.append(seat)