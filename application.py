from flask import request, redirect, render_template, flash, Flask


app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World" 