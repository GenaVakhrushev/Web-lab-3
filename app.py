from datetime import time
from flask import Flask, json, session, redirect, render_template, make_response, Response, request
import sqlite3

class Task:
    def __init__(self, id, title, description) -> None:
        self.id = id
        self.title = title
        self.description = description

app = Flask(__name__)
app.secret_key = 'fdfsdfgd'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/tasks/<user_id>')
def tasks(user_id):
    con = sqlite3.connect('web3.db')
    cur = con.cursor()

    task_list = [Task(row[0], row[1], row[2]) for row in cur.execute('select * from tasks where user_id = :user_id',dict(user_id = user_id)).fetchall()]

    return render_template('index.html', tasks=task_list)

@app.route('/api/check_pass',methods=["POST"])
def check_pass():
    json = request.json
    username = json['username']
    password = json['password']

    con = sqlite3.connect('web3.db')
    cur = con.cursor()

    user_id, db_pass = cur.execute('select id, password from users where username = :username',dict(username = username)).fetchone()

    if(password == db_pass):
        session['user_id'] = user_id
        return redirect(f'/tasks/{user_id}')
    else:
        return make_response("", 400)

@app.route('/api/register',methods=["POST"])
def register():
    json = request.json
    username = json['username']
    password = json['password']

    con = sqlite3.connect('web3.db')
    cur = con.cursor()

    try:
        cur.execute('insert into users(username, password) values (:username, :password)',dict(username = username, password = password))
        con.commit()
    except con.IntegrityError:
        return make_response("", 400)

    user_id = cur.lastrowid
    session['user_id'] = user_id

    return redirect(f'/tasks/{user_id}')

@app.route('/api/create_task',methods=["POST"])
def create_task():
    json = request.json
    title = json['title']
    description = json['description']
    con = sqlite3.connect('web3.db')
    cur = con.cursor()
    cur.execute('insert into tasks(title, description, user_id) values(:title,:description, :user_id)',dict(title = title,
                                                                                                            description = description,
                                                                                                            user_id = session['user_id']))
    con.commit()
    return make_response("", 200)

@app.route('/api/delete_task',methods=["POST"])
def delete_task():
    json = request.json
    id = json['id']
    con = sqlite3.connect('web3.db')
    cur = con.cursor()
    cur.execute('delete from tasks where id = :id',dict(id = id))
    con.commit()
    return make_response("", 200)

@app.route('/task/<id_task>')
def task(id_task):
    con = sqlite3.connect('web3.db')
    cur = con.cursor()

    title, description = cur.execute('select title, description from tasks where id = :id_task',dict(id_task=id_task)).fetchone()

    return render_template('task.html',title=title,description=description)