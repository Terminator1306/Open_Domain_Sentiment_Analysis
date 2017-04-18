# coding: utf-8
import MySQLdb


def connect(db_name='tmall'):
    db = MySQLdb.connect("127.0.0.1", "root", "12345", db_name)
    c = db.cursor()
    c.execute("set names utf8")
    return c

