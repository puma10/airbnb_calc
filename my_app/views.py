from flask import render_template
from my_app import app


@app.route("/")
def home():
    return render_template("calculator.html")
