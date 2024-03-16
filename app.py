from flask import Flask, render_template
from database import DBhandler
import sys

application = Flask(__name__)
application.config["SECRET_KEY"] = "greenpower"
DB = DBhandler()

@application.route("/")
def hello():
    return render_template("main.html")

@application.route("/login")
def login():
    return render_template("login.html")

@application.route("/todo")
def read_todo():
    return render_template("todo.html")

@application.route("/portfolio")
def read_total_portfolio():
    return render_template("total-portfolio.html")

if __name__ == "__main__":
    application.run(host='0.0.0.0')