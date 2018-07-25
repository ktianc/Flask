#coding=utf-8
from fabric.api import *

import os
import sys
import time


now = time.strftime("%y%m%d%H",time.localtime())

def apache(file_dir,remote_dir):

    with cd("/var/www/html"):
        run("zip -r {0}-{1}.zip {0}".format(file_dir,now))
        put("id_rsa","/var/www/html/")  #上传本地rsa到web服务器
        run("chmod -R 700 id_rsa")
        run("scp -q -i id_rsa {0}-{1}.zip root@47.104.86.129:/usr/local/nginx/html/backups/{2}/".format(file_dir,now,remote_dir))  #web server use ssh 进行传输
        run("rm -rf id_rsa")  #删除 web server rsa
        run("mv {0}-{1}.zip /tmp".format(file_dir,now))

def mysql(sql_name, remote_dir):
    with cd("/usr/local/"):
        run("mysqldump -uroot -pGy64100124 {0} > {0}-{1}.sql".format(sql_name,now))
        put("id_rsa", "/usr/local/")  # 上传本地rsa到web服务器
        run("chmod -R 700 id_rsa")
        run("scp -q -i id_rsa {0}-{1}.sql root@47.104.86.129:/usr/local/nginx/html/backups/{2}/".format(sql_name,now,remote_dir))  # web server use ssh 进行传输
        run("rm -rf id_rsa")  # 删除 web server rsa
        run("mv {0}-{1}.sql /tmp".format(sql_name,now))


