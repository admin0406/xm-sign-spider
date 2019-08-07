# *--conding:utf-8--*
import os
import random

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from config import API_TOKEN, MUSIC_PATH
import telebot
from telebot import types, logger
import requests
from data_comming import get_all_music_list, download
from models import *

requests.adapters.DEFAULT_RETRIES = 5
r = requests.session()
r.keep_alive = False
bot = telebot.TeleBot(token=API_TOKEN)


# 底部标签
def bottom_markup():
    markup = ReplyKeyboardMarkup()
    markup.row_width = 2
    markup.one_time_keyboard = 2
    markup.add(InlineKeyboardButton("💿热搜榜推荐", callback_data='recommend'),
               InlineKeyboardButton("🈲写代码专用", callback_data='very_hot'),
               InlineKeyboardButton("🎻小品相声", callback_data='classic_music'),
               InlineKeyboardButton("📗我要上传", callback_data='upload'))
    return markup

#
# # 卖家标签
# def seller_markup():
#     markup = InlineKeyboardMarkup()
#     markup.row_width = 2
#     markup.add(InlineKeyboardButton("今日出勤", callback_data='publish'),
#                InlineKeyboardButton("照片选人", callback_data='my_shelf'),
#                InlineKeyboardButton("交易完成", callback_data='all_rigth'),
#                InlineKeyboardButton("交易中", callback_data='transaction'),
#                InlineKeyboardButton("🙋🏻‍♂联系客服", url='t.me/bibo_dear'))
#     return markup
#
#
# # 买家标签
# def buyer_markup():
#     markup = InlineKeyboardMarkup()
#     markup.row_width = 2
#     markup.add(InlineKeyboardButton("个人详情", callback_data='user_info'),
#                InlineKeyboardButton("邀请链接", callback_data='my_link'),
#                InlineKeyboardButton("我买到的", callback_data='my_buy'))
#     return markup
#
#
# # 充值标签
# def recharge_markup():
#     markup = InlineKeyboardMarkup()
#     markup.row_width = 2
#     markup.add(InlineKeyboardButton("🏧充币", callback_data='recharge'),
#                InlineKeyboardButton("提币", callback_data='drawal'))
#     return markup


@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        bot.send_message(message.chat.id, "🌹欢迎来到天上一枝梅的音乐空间\n",
                         reply_markup=bottom_markup())

    except Exception as e:
        logger.error(e)
        pass


@bot.message_handler(func=lambda msg: msg.text)
def musin(message):
    try:
        if message.text == '💿热搜榜推荐':
            try:
                hot_list = search_db_by_hot(1)
                msg = '❤️可以输入歌名快速搜索\n热搜推荐:\n'
                for one in random.sample(hot_list, 20):
                    msg += "❤ `{}` \n".format(one[0])
                bot.send_message(message.chat.id, msg, parse_mode='Markdown')
            except Exception as e:
                logger.error(e)
                pass
        elif message.text == '🈲写代码专用':
            try:
                hot_list = search_db_by_hot(2)
                msg = '❤️可以输入歌名快速搜索\n写代码推荐:\n'
                for one in hot_list:
                    msg += "❤ `{}` \n".format(one[0])
                bot.send_message(message.chat.id, msg, parse_mode='Markdown')
            except Exception as e:
                logger.error(e)
                pass
        elif message.text == '🎻小品相声':
            try:
                hot_list = search_db_by_type('小品')
                msg = '❤️可以输入歌名快速搜索\n小品推荐:\n'
                for one in random.sample(hot_list, 20):
                    msg += "❤ `{}` \n".format(one[0])
                bot.send_message(message.chat.id, msg, parse_mode='Markdown')
            except Exception as e:
                logger.error(e)
                pass
        elif message.text == '📗我要上传':
            try:
                msg = bot.reply_to(message, '请输入你要上传的类型:\n'
                                            '`经典` `串烧` `小品`\n'
                                            'q 退出,可以复制`youtube`的链接直接上传\n'
                                            'youtube链接   一曲相思', parse_mode='Markdown')
                bot.register_next_step_handler(msg, get_user_input_type)
            except Exception as e:
                logger.error(e)
                pass

        else:
            name = message.text.strip()
            try:
                result = search_db(name)
                bot.send_message(message.chat.id, '[{}]({})'.format(result[0], result[1]), parse_mode='Markdown')
            except:
                music_list = get_all_music_list()
                if name+'.mp3' in music_list:
                    bot.reply_to(message,'正在发送....')
                    with open(MUSIC_PATH+'\\'+name+'.mp3','rb')as f:
                        bot.send_audio(message.chat.id,f,timeout=60)
                else:
                    bot.reply_to(message,'没有这首歌')
                    pass
    except Exception as e:
        logger.error(e)
        pass


lei_type = ['经典', '串烧', '小品']
user_dict = dict()


def get_user_input_type(message):
    if message.text.strip() in lei_type:
        user_dict['type'] = message.text
        mes = bot.reply_to(message, '请输入歌曲名称:(不能超过10个字)')
        bot.register_next_step_handler(mes, get_user_input_name)
    elif message.text.strip().upper() == 'Q':
        bot.reply_to(message, '退出成功，你现在可以输入歌名进行快速搜索额')
    elif message.text.startswith('http'):
        url ,name = message.text.strip().split()
        if name+'.mp3' not in get_all_music_list():
            bot.reply_to(message,'正在上传，请稍等.....')
            os.chdir(MUSIC_PATH)
            download(url, name)
            bot.reply_to(message,'上传成功')
        else:
            bot.reply_to(message,'已经存在，你可以直接输入歌名进行搜索')
            pass
    else:
        msg = bot.reply_to(message, '类型不存在，请[联系客服](t.me/bibo_dear)添加，或者重新输入',parse_mode='Markdown')
        bot.register_next_step_handler(msg, get_user_input_type)


def get_user_input_name(message):
    if len(message.text) > 10:
        msg = bot.reply_to(message, '名字太长，请重新输入')
        bot.register_next_step_handler(msg, get_user_input_name)
    elif message.text.strip().upper() == 'Q':
        bot.reply_to(message, '退出成功，你现在可以输入歌名进行快速搜索额')
    else:
        user_dict['name'] = message.text
        msg = bot.reply_to(message, '请拖入音频文件:')
        bot.register_next_step_handler(msg, save_user_input_file)


def save_user_input_file(message):
    if message.content_type == 'audio':
        user_dict['file_id'] = message.audio.file_id
        file = bot.get_file(file_id=message.audio.file_id)
        new_file = bot.download_file(file.file_path)
        with open('music_file\\{}.mp3'.format(user_dict['name']),'wb')as f:
            f.write(new_file)
        bot.reply_to(message,'上传成功！')
    elif message.text.strip().upper() == 'Q':
        bot.reply_to(message,'退出成功，你现在可以输入歌名进行快速搜索额')
    else:
        bot.reply_to(message, '上传的不是音频文件，请重新拖入文件上传！')


if __name__ == '__main__':
    bot.skip_pending = True
    bot.polling(none_stop=True)
