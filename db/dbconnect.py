# coding: utf-8
import MySQLdb


def connect(db_name='gp_web'):
    db = MySQLdb.connect("127.0.0.1", "root", "", db_name)
    db.set_character_set('utf8')
    c = db.cursor()
    c.execute("set names utf8")
    return db

