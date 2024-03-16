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

@application.route("/todo_insert")
def insert_todo():
    return render_template("todo_insert.html")

@application.route("/group_insert")
def insert_group_activity():
    return render_template("group_insert.html")

@application.route("/personal_insert")
def insert_personal_activity():
    return render_template("personal_insert.html")

if __name__ == "__main__":
    application.run(host='0.0.0.0')