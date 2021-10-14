from datetime import time
from flask import Flask, json, session, redirect, render_template, make_response, Response, request
import sqlite3

class Task:
    def __init__(self, id, title, description) -> None:
        self.id = id
        self.title = title
        self.description = description

app = Flask(__name__)

@app.route('/')
def home():
    con = sqlite3.connect('web3.db')
    cur = con.cursor()

    task_list = [Task(row[0], row[1], row[2]) for row in cur.execute('select * from tasks').fetchall()]

    return render_template('index.html', tasks=task_list)

@app.route('/api/create_task',methods=["POST"])
def create_task():
    json = request.json
    title = json['title']
    description = json['description']
    con = sqlite3.connect('web3.db')
    cur = con.cursor()
    cur.execute('insert into tasks(title, description) values(:title,:description)',dict(title = title,description = description))
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