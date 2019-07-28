# *--conding:utf-8--*
import sqlite3

with open('admin_list', 'r')as f:
    l = f.readlines()[0].split('|')
print(l)
user_name = '@shui99'

if user_name in l:
    print('df')