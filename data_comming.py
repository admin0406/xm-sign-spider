 # *--conding:utf-8--*
import re


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


def get_chat_id(message):
    return message.from_user.id


def get_user_shelf_and_save(msg):
    info = dict()
    info['chat_id'] = get_chat_id(msg)
    info['title'] = re.findall('标题:(.*)', msg.text)[0]
    info['description'] = re.findall('描述:(.*)', msg.text)[0]
    info['price'] = re.findall('价格:(\d{2,6})', msg.text)[0]
    return info
