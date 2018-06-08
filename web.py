#coding=utf-8

from flask import Flask,render_template
import config
app = Flask(__name__)
app.config.from_object(config)

@app.route("/")
def index():
    return "<p style='color:red;'>Programming enrich life!</p>"

@app.route('/<int:parameter>/')
def login(parameter):
    test_d = {"k":"tianc","life":"Beautiful"}
    if parameter:
        return render_template("index.html",test = test_d["k"])
    else:
        return render_template("index.html",test = test_d["life"])

if __name__ == '__main__':
    app.run()
