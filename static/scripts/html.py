#coding=utf-8
from fabric.api import *

import os
import sys
import time


now = time.strftime("%y%m%d%H",time.localtime())

def apache(file_dir,remote_dir):

    with cd("/var/www/html"):
        run("zip -r {0}-{1}.zip {0}".format(file_dir,now))
        get("{0}-{1}.zip".format(file_dir,now),"/usr/local/nginx/html/backups/{2}/".format(remote_dir))
        run("mv {0}-{1}.zip /tmp".format(file_dir,now))

def mysql(sql_name, remote_dir):
    with cd("/usr/local/"):
        run("mysqldump -uroot -pGy64100124 {0} > {0}-{1}.sql".format(sql_name,now))
        get("{0}-{1}.sql".format(sql_name,now),"/usr/local/nginx/html/backups/{0}/".format(remote_dir))
        run("rm -rf {0}-{1}.sql".format(sql_name,now))

