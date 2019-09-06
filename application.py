from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request,url_for,session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required,luhn_algorithm, naira

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
    #return apology("you need to work on the booking page", 400)
    arrivals = db.execute("SELECT arrival FROM terminals WHERE depature=:Lagos",Lagos="Lagos")
    return render_template("booking.html", arrivals=arrivals)

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


@app.route("/logout")
def logout():

    # clear user_id session
    session.clear()

    # redirect to the login page
    return redirect("/login")


#listening for the register route
@app.route("/register", methods=["GET","POST"])
def register():
    #check if the route was entered via POST
    if request.method == "POST":
        #check if all fields were properly filled 
        if not request.form.get("firstName"):
            return apology("you omitted your firstname", 400) #note, this is yet to be implemented
        elif not request.form.get("lastName"):
            return apology("you omitted your lastname", 400)
        elif not request.form.get("email"):
            return apology("you omitted your email", 400)
        elif not request.form.get("phoneNumber"):
            return apology("you omitted your phone number", 400)
        elif not request.form.get("password"):
            return apology("you must enter a password", 400)
        elif not request.form.get("password") == request.form.get("confirmation"): #check what was used for the input name
            return apology("passwords do not match", 400)
        # generate a hash for the password
        hash = generate_password_hash(request.form.get("password"))
        #insert the form values into the database
        new_user = db.execute("INSERT INTO users (phone, firstname, lastname, email, hash) VALUES (:phone, :firstname, :lastname, :email, :hash)", phone=request.form.get("phoneNumber"), firstname=request.form.get("firstName"), lastname=request.form.get("lastName"), email=request.form.get("email"), hash=hash)
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
#use this if the booking page will be different from the seat-selection page
all_arr = []


@app.route("/booking", methods=["GET","POST"])
def booking():
    if request.method == "POST":
        terminal = request.form.get("terminal") 
        date = request.form.get("date")
        credit_card = request.form.get("creditCard") #verify the name that was used
        amount = request.form.get("price")
        seat = request.form.get("seat")
        if not terminal:
            return apology("you did not enter your destination", 400)
        elif not date:
            return apology("you did not enter a date", 400)
        elif not credit_card:
            return apology("you must enter your credit card details", 400)
        validate_card = luhn_algorithm(credit_card)
        if validate_card == True:
            trans = db.execute("INSERT INTO transactions (id, terminal, date, seat, amount) VALUES (:id, :terminal, :date, :seat, :amount)", id=session["user_id"], terminal=terminal, date=date, seat=seat, amount=8500)
            if not trans:
                return apology("you omitted at least one field", 400)
            else:
                flash("you have successfully booked a seat. check your email for details")
                all_arr.append(seat)
                return redirect(url_for("index"))
        else:
            flash("invalid card details")
            return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))


@app.route('/seatselect', methods=["POST"])
def seatselect():

    info = request.get_json()

    print(info)

@app.route("/checkprice", methods=["GET"])
def checkprice():
    arrival = request.args.get("arrival")
    rows = db.execute("SELECT price FROM terminals WHERE arrival=:arrival", arrival=arrival)
    price = naira(rows[0]["price"])
    return jsonify(price)


def errorhandler(e):
    """Handle error"""
    
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

