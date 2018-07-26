#coding=utf-8

from flask import Flask,render_template,url_for,redirect,request
#导入flask类，这个类的势力是WSGI应用程序
from flask_sqlalchemy import SQLAlchemy #导入SQLAlchemy类
from werkzeug.utils import secure_filename
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
    host_ip = db.Column(db.String(50),nullable=False)
    host_user = db.Column(db.String(50),nullable=False)
    host_password = db.Column(db.String(50),nullable=False)
    host_key = db.Column(db.String(50),unique=True)

db.create_all()   #创建所有表




@app.route("/",methods=["GET","POST"])  #route装饰器，访问/触发index,传递methods参数改变请求方式
def index():  #编辑主页数据
    if request.method == "POST": #请求方式为POST触发
        project_list = []
        key_list = []
        for x in db.session.execute("select project from backups").fetchall():
            project_list.append(x.project)
        for y in db.session.execute("select host_key from backups").fetchall():
            key_list.append(y.host_key)
        project_name = request.form["project_name"] #获取form表格中的project_name
        if project_name not in project_list:   #如果没有这个项目名
            webserver = request.form["webserver"]  #获得用户输入的数据
            localname = request.form["localname"]
            remotedir = request.form["remotedir"]
            host = request.form["host"]
            user = request.form["user"]
            password = request.form["password"]
            try:  #检测以下语句
                file = request.files["file"] #获得用户上传文件
                filename = secure_filename(file.filename)  # 检测，过滤掉中文名,进行解码

                if filename in key_list:  #如果用户上传的密钥文件存在，则报错
                    return render_template("Error.html", error_hint=u"密钥名称重复，请更换名称")

                else: #否则，上传文件，并保存数据库
                    file.save('{0}/static/scripts/{1}'.format(os.path.dirname(__file__), filename))  # 保存上传的文件

                    db.session.add(backups(project=project_name,  # 添加到数据库
                                           client_webserver=webserver,
                                           client_dirname=localname,
                                           server_dirname=remotedir,
                                           host_ip=host,
                                           host_user=user,
                                           host_password=password,
                                           host_key=file.filename))

                    db.session.commit()  # 提交
            except:  #用户没有上传文件会报错执行下面
                db.session.add(backups(project=project_name,
                                       client_webserver=webserver,
                                       client_dirname=localname,
                                       server_dirname=remotedir,
                                       host_ip=host,
                                       host_user=user,
                                       host_password=password))

                db.session.commit()  # 提交


        else:  #如果有重复项目名，执行
            return render_template("index.html",Error="Error:The project name cannot be repeated")

    return render_template("index.html")  #请求方式为get返回indexhtml，渲染模板



@app.route('/project',methods=["GET","POST"])  #传递methods参数改变请求方式
def project():
    project_list = []
    for x in db.session.execute("select project from backups").fetchall():  #循环查询到的project列的数据
        project_list.append(x.project)  #添加到列表

    if request.method=="POST":  #如果请求方式为post
        option = request.form["operation"]   #获得用户单选的值
        input_project = request.form["project"]  #获得用户数据的项目名
        if input_project in project_list:  #如果项目名在列表中，执行

            if option == "delete":  #用户选择delete
                db.session.delete(backups.query.filter(backups.project == input_project).first()) #删除用户输入的第一条项目名
                db.session.commit()  #提交
                return redirect(url_for('project'))   #重定向此页面

            elif option == "backup":   #用户选择backup，获取数据库信息
                IP = db.session.execute("select host_ip from backups where project = '{0}' ".format(input_project)).fetchall()[0].host_ip
                USER = db.session.execute("select host_user from backups where project = '{0}' ".format(input_project)).fetchall()[0].host_user
                PASSWORD = db.session.execute("select host_password from backups where project = '{0}' ".format(input_project)).fetchall()[0].host_password
                KEY_FILE = db.session.execute("select host_key from backups where project = '{0}' ".format(input_project)).fetchall()[0].host_key
                WEB = db.session.execute("select client_webserver from backups where project = '{0}' ".format(input_project)).fetchall()[0].client_webserver
                CLIENT = db.session.execute("select client_dirname from backups where project = '{0}' ".format(input_project)).fetchall()[0].client_dirname
                SERVER = db.session.execute("select server_dirname from backups where project = '{0}' ".format(input_project)).fetchall()[0].server_dirname

                #fab -f service.py -H xxx:22 -u xxx -p xxx -i xxx.rsa service:client,server
                os.chdir("/usr/local/backups/static/scripts/") #更改execult directory

                if not KEY_FILE: #如果密钥文件为空执行
                    os.system("fab -f html.py -H '{0}:22' -u {1} -p {2} {3}:{4},{5}".format(IP,USER,PASSWORD,WEB,CLIENT,SERVER))
                else: #如果密钥文件不为空执行
                    os.system("fab -f html.py -H '{0}:22' -u {1} -p {2} -i {3} {4}:{5},{6}".format(IP,USER,PASSWORD,KEY_FILE,WEB,CLIENT,SERVER))



        else: #如果输入需要操作的项目名不存在
            return render_template("project.html",projectname = project_list,Error=u"输入的项目名称不存在")

    return render_template("project.html",projectname = project_list)  #渲染模板，并传送列表



if __name__ == '__main__':#只有当该脚本被python解释其直接执行才会运行
    app.run()  #运行app应用在本地服务器
