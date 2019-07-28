# *--conding:utf-8--*
import datetime
import sqlite3
import threading
from config import API_TOKEN, URL, admin_path, black_path, address_path
import telebot
from telebot import types
from logger import Logger
import requests
import time
import join, re
import os
from data_comming import *

requests.adapters.DEFAULT_RETRIES = 5
r = requests.session()
r.keep_alive = False
bot = telebot.TeleBot(token=API_TOKEN)
logger = Logger().logger

PATH = os.getcwd()


# 获取管理员列表
def is_admin():
    with open(admin_path, 'r', encoding='utf-8')as f:
        return list(i.strip() for i in f.read().strip().split('|'))


# 获取黑名单列表
def is_black():
    with open(black_path, 'r', encoding='utf-8')as f:
        return list(i.strip() for i in f.read().strip().split('|'))


# 添加权限
@bot.message_handler(commands=['set_admin'], func=lambda msg: msg.reply_to_message)
def set_admin(message):
    try:
        user_id = message.reply_to_message.from_user.id
        if str(message.from_user.id) in is_admin():
            if str(user_id) not in is_admin() and user_id != bot.get_me().id:
                with open(admin_path, 'a', encoding='utf-8')as f:
                    f.write('|' +str(user_id))
                bot.send_message(message.chat.id, '添加权限成功')
            else:
                bot.send_message(message.chat.id, '如果本 `bot` 没猜错，此人已有超级权限，要不就是进了黑名单', parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, '多半是权限不够，加油吧骚年')
    except:
        pass


# 设置黑名单并禁言10分钟
@bot.message_handler(commands=['set_black'], func=lambda msg: msg.reply_to_message)
def set_black_list(message):
    try:
        logger.info(message.text)
        user_id = message.reply_to_message.from_user.id
        if str(message.from_user.id) in is_admin():
            if user_id not in is_admin() and user_id != bot.get_me().id:
                with open(black_path, 'a', encoding='utf-8')as f:
                    f.write('|' + str(user_id))
                bot.restrict_chat_member(message.chat.id, user_id, until_date=time.time() + 600)
                bot.send_message(message.chat.id, '禁言10分钟，警告一次')
            else:
                bot.send_message(message.chat.id, '你不能禁言此用户额')
        else:
            bot.send_message(message.chat.id, '如果本`bot` 没猜错 多半是你 权限不够，加油吧骚年', parse_mode='Markdown')
    except Exception as e:
        logger.error(e)


# 踢人
@bot.message_handler(commands=['ban'], func=lambda msg: msg.reply_to_message)
def ban_user(message):
    try:
        logger.info(message.text)
        user_id = message.reply_to_message.from_user.id
        if str(message.from_user.id) in is_admin() and user_id not in is_admin() and user_id != bot.get_me().id:
            bot.kick_chat_member(message.chat.id, user_id)
        else:
            bot.send_message(message.chat.id,'如果本`bot` 没猜错 多半是你 权限不够，加油吧骚年', parse_mode='Markdown')
    except Exception as e:
        logger.error(e)


@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        logger.info(message.text)
        keyboard = types.InlineKeyboardMarkup()
        callback_button_menu = types.InlineKeyboardButton(text="讲段子", callback_data="讲段子", )
        callback_button_song = types.InlineKeyboardButton(text='天气状况', callback_data='天气状况')
        callback_button_phones = types.InlineKeyboardButton(text='电话簿',
                                                            url='https://www.feituan.ph/index.php?cid=&ccid=9')
        callback_button_car1 = types.InlineKeyboardButton(text='气质女王组', url='t.me/phgdjz')
        callback_button_car2 = types.InlineKeyboardButton(text='清纯萝莉范', url='t.me/phhrg')
        keyboard.add(callback_button_menu, callback_button_song, callback_button_phones, callback_button_car1,
                     callback_button_car2)
        msg_id = bot.send_message(message.chat.id, "👌👈欢迎使用自助机器人👌👈!", reply_markup=keyboard).message_id
        timer = threading.Timer(300, bot.delete_message, (message.chat.id, msg_id))
        timer.start()
    except Exception as e:
        logger.error(e)


# 用户获取地址
@bot.message_handler(commands=['get_addr'])
def get_address(message):
    try:
        with open(address_path, 'r', encoding='utf-8')as f:
            data = f.readlines()[0].strip()
        bot.send_message(message.chat.id, data)
    except:
        pass


# 设置地址
@bot.message_handler(regexp='set_addr\s+(.*)_over')
def set_address(message):
    try:
        addrs = re.search('set_addr\s+(.*)_over', message.text).group(1)
        with open('address', 'w', encoding='utf-8')as f:
            f.write(addrs)
        bot.send_message(message.chat.id, '设置成功')
    except:
        pass

# 进群欢迎信息
@bot.message_handler(content_types=['new_chat_members', 'left_chat_member'])
def say_welcom(message):
    try:
        if message.new_chat_members:
            frist_name = message.new_chat_member.first_name
            last_name = message.new_chat_member.last_name
            if frist_name and last_name and frist_name != last_name:
                nick_name = frist_name + last_name
            else:
                nick_name = frist_name
            logger.info(message.new_chat_member)
            msg_id = bot.send_message(message.chat.id,
                                      "💋AE86热烈欢迎新成员: {} 加入大家庭\n🌺 کارب عزیز  🌺\n"
                                      "你可以把本[bot](t.me/@Bibo_dear2_bot)加到[你的群组](t.me/YoutubeChannelsBot?startgroup=true)里面".format(
                                          nick_name), parse_mode='Markdown').message_id
            timer = threading.Timer(20, bot.delete_message, (message.chat.id, msg_id))
            timer.start()

        else:
            frist_name = message.left_chat_member.first_name
            last_name = message.left_chat_member.last_name
            if frist_name and last_name and frist_name != last_name:
                nick_name = frist_name+last_name
            else:
                nick_name=frist_name
            logger.info(message.left_chat_member)
            msg_id = bot.send_message(message.chat.id,
                                      '本群精英:{} 离开了我们团队，一路走好，恭喜发财！'.format(
                                          nick_name)).message_id
            timer = threading.Timer(20, bot.delete_message, (message.chat.id, msg_id))
            timer.start()
    except Exception as e:
        logger.error(e)


# 天气状况
@bot.callback_query_handler(func=lambda call: call.data == '天气状况')
def callback_menu(call):
    try:
        data = get_weather()
        logger.info(call.from_user)
        logger.info(call.data)
        callback_id = call.message.json['chat']['id']
        msg_id = bot.send_message(callback_id,
                                  "城市{} 温度:{} {} \n风向:{}{} 湿度:{} 时间:{}\n 60秒后自动删除！".format(data['address'],
                                                                                           data['temp'],
                                                                                           data['weather'],
                                                                                           data['windDirection'],
                                                                                           data['windPower'],
                                                                                           data['humidity'],
                                                                                           data[
                                                                                               'reportTime'])).message_id
        timer = threading.Timer(60, bot.delete_message, (callback_id, msg_id))
        timer.start()
    except Exception as e:
        logger.error(e)


# 段子笑话
@bot.callback_query_handler(func=lambda call: call.data == '讲段子')
def callback_menu(call):
    try:
        logger.info(call.data)
        callback_id = call.message.json['chat']['id']
        msg_id = bot.send_message(callback_id, get_joke()).message_id
        timer = threading.Timer(300, bot.delete_message, (callback_id, msg_id))
        timer.start()
    except Exception as e:
        logger.error(e)



# 查看个人信息
@bot.message_handler(commands=['my_id'])
def get_user_info(message):
    try:
        logger.info(message.text)
        nick_name = get_nickname(message)
        if message.from_user.username:
            msg_id = bot.send_message(message.chat.id,
                                      "亲爱的❤️{}  ❤️你好\n你的 Chat_Id = {}\nUsername是 {} \n"
                                      "你可以把本[bot](t.me/@Bibo_dear_bot)加到[你的群组](t.me/YoutubeChannelsBot?startgroup=true)里面\n"
                                      "  10秒后自动删除！\n".format(nick_name,
                                                             message.from_user.id,
                                                             message.from_user.username),
                                      parse_mode='Markdown').message_id
            timer = threading.Timer(10, bot.delete_message, (message.chat.id, msg_id))
            timer.start()
        else:
            msg_id = bot.send_message(message.chat.id,
                                      "亲爱的 {} 你好\n你的 Chat_Id是 = {}\nUsername 还没设置 \n  10秒后自动删除！".format(
                                          message.from_user.first_name,
                                          message.from_user.id)).message_id
            timer = threading.Timer(10, bot.delete_message, (message.chat.id, msg_id))
            timer.start()

    except Exception as e:
        logger.error(e)


# 获取游戏帮助
@bot.message_handler(commands=['game_help'])
def get_help(message):
    try:
        logger.info(message.chat)
        if message.chat.type == 'private':
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id,
                             "/join_lottery - 加入抽奖\n/list_lottery- 查看名单\n/lottery - 抽奖[admin]\n/clear_game_list - 清空名单[admin]\n")
        else:
            bot.send_chat_action(message.chat.id, 'typing')
            msg_id = bot.send_message(message.chat.id,
                                      "/join_lottery - 加入抽奖\n/list_lottery- 查看名单\n/lottery - 抽奖[admin]\n/clear_game_list - 清空名单[admin]\n").message_id
            timer = threading.Timer(30, bot.delete_message, (message.chat.id, msg_id))
            timer.start()
    except Exception as e:
        logger.error(e)


# 加入抽奖
@bot.message_handler(commands=['join_lottery'])
def join_lottery(message):
    try:
        logger.info(message.chat)
        if message.chat.type == 'private':
            un = message.from_user.username
            r = join.add_in(un)
            bot.reply_to(message, r)
        else:
            un = message.from_user.username
            r = join.add_in(un)
            msg_id = bot.reply_to(message, r).message_id
            timer = threading.Timer(15, bot.delete_message, (message.chat.id, msg_id))
            timer.start()
    except Exception as e:
        logger.error(e)


# 查看抽奖名单
@bot.message_handler(commands=['list_lottery'])
def send_list(message):
    try:
        logger.info(message.chat)
        if message.chat.type == 'private':
            un = message.from_user.username
            bot.send_chat_action(message.chat.id, 'typing')
            r = join.read_list(un)
            count = -1
            for count, line in enumerate(open("list", 'r')):
                pass
            count += 1
            rr = u'%s \n\n 目前共有%s人参与抽奖哦' % (r, count)
            msg_id = bot.reply_to(message, rr).message_id
            timer = threading.Timer(10, bot.delete_message, (message.chat.id, msg_id))
            timer.start()

        else:
            bot.send_chat_action(message.chat.id, 'typing')
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton('戳这里！', url='https://t.me/Bibo_dear2_bot')
            markup.add(btn)
            msg_id = bot.send_message(chat_id=message.chat.id, text=u'为了防止刷屏，请在私聊中使用此命令哦～',
                                      reply_markup=markup).message_id
            timer = threading.Timer(10, bot.delete_message, (message.chat.id, msg_id))
            timer.start()
    except Exception as e:
        logger.error(e)


# 抽奖
@bot.message_handler(commands=['lottery'])
def execution_lottery(message):
    try:
        un = message.from_user.username
        logger.info(message.chat)
        f = open('admin_list', 'r')
        l = f.read()
        if l.find('%s' % un) == -1:
            msg_id = bot.send_message(message.chat.id,
                                      "你好:\n由于你权限不够还不能操作额\n"
                                      "你可以把本[bot](t.me/@Bibo_dear2_bot)加到[你的群组](t.me/YoutubeChannelsBot?startgroup=true)里面",
                                      parse_mode='Markdown').message_id
            timer = threading.Timer(10, bot.delete_message, (message.chat.id, msg_id))
            timer.start()
        else:
            code, r = join.get_lottery()
            bot.reply_to(message, r)
    except Exception as e:
        logger.error(e)


# 清空名单
@bot.message_handler(commands=['clear_game_list'])
def del_lottery_list(message):
    try:
        un = message.from_user.username
        logger.info(message.chat)
        f = open('admin_list', 'r')
        l = f.read()
        if message.chat.type == 'private':
            if l.find('%s' % un) == -1:
                bot.send_message(message.chat.id,
                                 "你好:\n由于你权限不够还不能操作额\n"
                                 "你可以把本[bot](t.me/@Bibo_dear2_bot)加到[你的群组](t.me/YoutubeChannelsBot?startgroup=true)里面",
                                 parse_mode='Markdown')
            else:
                r = join.del_list()
                bot.reply_to(message, r)
        else:
            if l.find('%s' % un) == -1:
                msg_id = bot.send_message(message.chat.id,
                                          "你好:\n由于你权限不够还不能操作额\n"
                                          "你可以把本[bot](t.me/@Bibo_dear_bot)加到[你的群组](t.me/YoutubeChannelsBot?startgroup=true)里面",
                                          parse_mode='Markdown').message_id
                timer = threading.Timer(10, bot.delete_message, (message.chat.id, msg_id))
                timer.start()
            else:
                r = join.del_list()
                msg_id = bot.reply_to(message, r).message_id
                timer = threading.Timer(5, bot.delete_message, (message.chat.id, msg_id))
                timer.start()
    except Exception as e:
        logger.error(e)


@bot.message_handler(commands=['sign'])
def user_sign(message):
    logger.info(message.chat)
    try:
        username = get_nickname(message)
        chat_id = message.from_user.id
        t = str(datetime.datetime.today()).split(' ')[0]
        t1 = search_last_sign_time(chat_id)
        if t1 and t == str(t1).split(' ')[0]:
            msg_id = bot.reply_to(message, '今日已签到,签到时间为:{} 请明天再来！20秒自毁以启动'.format(t1)).message_id
            timer = threading.Timer(20, bot.delete_message, (message.chat.id, msg_id))
            timer.start()
        else:
            insert_sign(username, chat_id)
            msg_id = bot.reply_to(message, '亲爱的 {} 恭喜你签到成功! 20秒自毁以启动'.format(username)).message_id
            timer = threading.Timer(20, bot.delete_message, (message.chat.id, msg_id))
            timer.start()
    except Exception as e:
        logger.error(e)


@bot.message_handler(commands=['mystats'])
def user_status(message):
    try:
        logger.info(message.chat)
        username = get_nickname(message)
        chat_id = message.from_user.id
        num = search_signs(chat_id)
        msg_id = bot.reply_to(message, '{}:您总共签到:{} 次，很棒棒额，请再接再厉，20秒自毁以启动'.format(username, num)).message_id
        timer = threading.Timer(20, bot.delete_message, (message.chat.id, msg_id))
        timer.start()
    except Exception as e:
        logger.error(e)


def get_joke():
    res = r.get(URL['joke_url'])
    if res.status_code == 200:
        return res.json()['data'][0]['content']


def get_weather():
    res = r.get(URL['weather_url']).json()
    return res['data']


if __name__ == '__main__':
    bot.skip_pending = True
    bot.polling(none_stop=True)
