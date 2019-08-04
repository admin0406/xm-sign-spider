# *--conding:utf-8--*
import telebot
from config import API_TOKEN
from data_comming import *

bot = telebot.TeleBot(API_TOKEN)


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



if __name__ == '__main__':
    bot.polling(none_stop=True)
