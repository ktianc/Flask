#coding=utf-8

from flask import Flask,render_template,url_for,redirect,request
#导入flask类，这个类的势力是WSGI应用程序
from flask_sqlalchemy import SQLAlchemy #导入SQLAlchemy类
import config   #导入config配置文件
import os
import json   #导入json，可以编码和解码
app = Flask(__name__) #创建flask类的实例
app.config.from_object(config)  #加载配置
db = SQLAlchemy(app) #创建SQLAlchemy类的实例


class backups(db.Model):  #创建backups表模型
    id = db.Column(db.Integer,primary_key=True,autoincrement=True) #创建id列，自动增长，主键
    project = db.Column(db.String(50),nullable=False,unique=True)  #创建project列，不能为空，不能重复
    client_webserver = db.Column(db.String(50),nullable=False)
    client_dirname = db.Column(db.String(50),nullable=False)
    server_dirname = db.Column(db.String(50),nullable=False)

db.create_all()   #创建所有表


@app.route("/",methods=["GET","POST"])  #route装饰器，访问/触发index
def index():  #编辑主页数据
    if request.method == "POST": #请求方式为POST触发
        project_name = request.form["project_name"] #获取form表格中的project_name
        webserver = request.form["webserver"]
        localname = request.form["localname"]
        remotedir = request.form["remotedir"]
        db.session.add(backups(project=project_name,client_webserver=webserver,client_dirname=localname,server_dirname=remotedir))
        #添加数据到数据库
        db.session.commit() #提交

    project_list = []
    # for x in backups.query.filter(backups.project).all():
    #查询project列不为aaa的所有数据
    for x in db.session.execute("select project from backups").fetchall():
        project_list.append(x.project)


    return render_template("index.html",projectname = project_list)



if __name__ == '__main__':#只有当该脚本被python解释其直接执行才会运行
    app.run(host="0.0.0.0")  #运行app应用在本地服务器
