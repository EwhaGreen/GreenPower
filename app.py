from flask import Flask, render_template, request, session, redirect, url_for, flash
from database import DBhandler
import hashlib
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

@application.route("/login_confirm", methods=['POST'])
def login_user():
    id = request.form['id']
    password = request.form['password']
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    user_found, user_name = DB.find_user(id, password_hash)
    if user_found:
        session['id'] = id
        session['name'] = user_name
        return render_template("main.html")
    else:
        error_message = "잘못된 ID 혹은 password를 입력하셨습니다."
        return render_template("login.html", error=error_message)
        

if __name__ == "__main__":
    application.run(host='0.0.0.0')