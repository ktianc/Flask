#coding=utf-8

from flask import Flask,render_template,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
import config
app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login/")
def login():
    return render_template("login.html")

if __name__ == '__main__':
    app.run()
