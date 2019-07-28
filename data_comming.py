# *--conding:utf-8--*
import sqlite3

import yaml


def get_username(message):
    if message.from_user.username:
        return message.from_user.username
    else:
        return ''


def get_nickname(message):
    frist_name = message.from_user.first_name
    last_name = message.from_user.last_name
    if frist_name and last_name and frist_name != last_name:
        username = frist_name + last_name
    else:
        username = frist_name
    return username


# 见表
def creat_table():
    """创建表"""
    conncet = sqlite3.connect('telegram_user')
    curs = conncet.cursor()
    curs.execute(
        "create table User_messages(id integer PRIMARY KEY AUTOINCREMENT,nick_name varchar(255),chat_id int(11),send_time TIMESTAMP default (datetime('now','localtime')))")

    curs.close()
    conncet.close()


# 插入数据库签到表
def insert_sign(telegram_user_name, chat_id):
    sql = "insert into User_sign(user_name,chat_id) values ('{}','{}');".format(
        telegram_user_name, chat_id)
    conn = sqlite3.connect('telegram_user')
    cur = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
        return cur.rowcount
    except:
        conn.rollback()
    finally:
        cur.close()
        conn.close()


# 查询累计签到
def search_signs(chat_id):
    sql = "SELECT COUNT(1) from User_sign WHERE chat_id =='{}';".format(chat_id)
    conn = sqlite3.connect('telegram_user')
    cur = conn.cursor()
    try:
        cur.execute(sql)
        return cur.fetchone()[0]
    except:
        pass
    finally:
        cur.close()
        conn.close()


# 查询最后一次签到的时间
def search_last_sign_time(chat_id):
    sql = "SELECT sign_time from User_sign WHERE chat_id ='{}' order by  id desc limit 1;".format(chat_id)
    conn = sqlite3.connect('telegram_user')
    cur = conn.cursor()
    try:
        cur.execute(sql)
        return cur.fetchone()[0]
    except:
        pass
    finally:
        cur.close()
        conn.close()


def save_text_to_sql(nick_name, chat_id, new_chat_member='0', left_chat_member='0', text='', other='0'):
    sql = "insert into User_messages(nick_name,chat_id,new_chat_member,left_chat_member,text,other) values ('{}','{}','{}','{}','{}','{}');".format(
        nick_name, chat_id, new_chat_member, left_chat_member, text, other)
    with sqlite3.connect('telegram_user')as conn:
        conn.cursor().execute(sql)
