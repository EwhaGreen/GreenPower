from flask import Flask, render_template, request, session, redirect, url_for, flash
from database import DBhandler
import hashlib
import sys

application = Flask(__name__)
application.config["SECRET_KEY"] = "greenpower"
DB = DBhandler()

# 라우팅
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
def read_todo_portfolio():
    return render_template("todo_portfolio.html")

@application.route("/todo_insert")
def insert_todo():
    return render_template("todo_insert.html")

@application.route("/group_insert")
def insert_group_activity():
    return render_template("group_insert.html")

@application.route("/personal_insert")
def insert_personal_activity():
    return render_template("personal_insert.html")


# 로그인
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


# group_activity db 전송
@application.route("/add_group_activity", methods=['POST'])
def add_group_activity():
    activity_kind = request.form['activity_kind']
    activity_name = request.form['activity_name']

    DB.add_group_activity(activity_kind, activity_name)

    flash('단체 활동이 성공적으로 등록되었습니다.')
    return redirect(url_for('read_todo'))
    
# personal_activity db 전송
@application.route("/add_personal_activity", methods=['POST'])
def add_personal_activity():
    activity_kind = request.form['activity_kind']
    activity_name = request.form['activity_name']

    DB.add_personal_activity(activity_kind, activity_name)

    flash('개인 활동이 성공적으로 등록되었습니다.')
    return redirect(url_for('read_todo'))
    
if __name__ == "__main__":
    application.run(host='0.0.0.0')