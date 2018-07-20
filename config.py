#coding=utf-8

DEBUG=True

# dialect+driver://username:password@host:port/database

HOST = "47.104.86.129"
DIRLECT = "mysql"
DRIVER = "mysqldb"
USERNAME = "root"
PASSWD = "ktianc"
PORT = 3306
DATABASE = "web_backups"

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIRLECT,DRIVER,USERNAME,PASSWD,HOST,PORT,DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False