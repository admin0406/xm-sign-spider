# *--conding:utf-8--*
import threading
import time

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from config import API_TOKEN
import telebot
from telebot import types, logger
import requests
from data_comming import *
from sqlalchemy import create_engine, and_
from models import *

requests.adapters.DEFAULT_RETRIES = 5
r = requests.session()
r.keep_alive = False
bot = telebot.TeleBot(token=API_TOKEN)


# 底部标签
def bottom_markup():
    markup = ReplyKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("👤买家中心", callback_data='buyer'),
               InlineKeyboardButton("🤵卖家中心", callback_data='seller'),
               InlineKeyboardButton("🏧充币/提币", callback_data='coin'),
               InlineKeyboardButton("🙋🏻‍♂️联系客服", callback_data='customer')
               )
    return markup


# 卖家标签
def seller_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("发布商品", callback_data='publish'),
               InlineKeyboardButton("我的货架", callback_data='my_shelf'),
               InlineKeyboardButton("交易完成", callback_data='all_rigth'),
               InlineKeyboardButton("交易中", callback_data='transaction'))
    return markup


# 买家标签
def buyer_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("个人详情", callback_data='user_info'),
               InlineKeyboardButton("邀请链接", callback_data='my_link'),
               InlineKeyboardButton("我买到的", callback_data='my_buy'))
    return markup


# 充值标签
def recharge_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("🏧充币", callback_data='recharge'),
               InlineKeyboardButton("提币", callback_data='drawal'))
    return markup


user_dict = dict()


@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        bot.send_message(message.chat.id, "🌹欢迎来到8号商城,发送关键字可以搜索商品\n".format(get_nickname(message)),
                         reply_markup=bottom_markup())

    except Exception as e:
        logger.error(e)


@bot.message_handler(func=lambda msg: msg.text == '👤买家中心')
def get_buyer_info(msg):
    try:
        bot.send_message(msg.chat.id, "欢迎!你的可用余额:0BTC\n"
                                      "⚠️点击个人详情备份你的账号密钥,当你的Telegram账号无法登录你可以使用密钥进行账号找回\n"
                                      "⚠️当其他人使用你的推广链接注册并完成交易可以获取积分,可以换取权益或BTC\n"
                                      "⚠️点击我买到的可以查看✅已完成和⚠️未完成的订单", reply_markup=buyer_markup())
    except Exception as e:
        logger.error(e)


@bot.message_handler(func=lambda msg: msg.text == '🤵卖家中心')
def get_buyer_info(msg):
    try:
        bot.send_message(msg.chat.id, "欢迎!你的余额:0BTC\n"
                                      "在闲鱼你可以出售任何服务/数据,比特币数量根据付款当时的汇率换算,让你不用担心币价浮动", reply_markup=seller_markup())
    except Exception as e:
        logger.error(e)


# 发布商品
@bot.callback_query_handler(func=lambda call: call.data == 'publish')
def publish(call):
    try:
        user_dict['chat_id'] = call.from_user.id
        msg = bot.reply_to(call.message, "请输入商品标题:(不能超过30个字)")
        bot.register_next_step_handler(msg, get_user_input_title)
    except Exception as e:
        logger.error(e)


# 接受用户输入标题
def get_user_input_title(message):
    try:
        if len(message.text) < 31:
            user_dict['title'] = message.text
            msg = bot.reply_to(message, '请输入商品描述:')
            bot.register_next_step_handler(msg, get_user_input_description)
        else:
            msg = bot.reply_to(message, '标题过长，请重新输入:(不能超过30个字)')
            bot.register_next_step_handler(msg, get_user_input_title)
    except Exception as e:
        logger.error(e)


# 接受用户输入描述信息
def get_user_input_description(message):
    try:
        if len(message.text) < 201:
            user_dict['description'] = message.text
            msg = bot.reply_to(message, '请输入商品价格:(10-10万的整数)')
            bot.register_next_step_handler(msg, get_user_input_price)
        else:
            msg = bot.reply_to(message, '超出限制，请重新输入:')
            bot.register_next_step_handler(msg, get_user_input_description)
    except Exception as e:
        logger.error(e)


# 接受用户输入价格
def get_user_input_price(message):
    try:
        if not message.text.isdigit() or int(message.text) < 10 or int(message.text) > 100000:
            msg = bot.reply_to(message, '输入错误，请重新输入:(10-10万的整数)')
            bot.register_next_step_handler(msg, get_user_input_price)
        else:
            user_dict['price'] = int(message.text)
            msg = bot.reply_to(message, "您输入的信息为:\n"
                                        "标题:{}\n"
                                        "描述:{}\n"
                                        "价格:{}\n"
                                        '确认无误请输入:1'.format(user_dict['title'], user_dict['description'],
                                                           user_dict['price']))

            bot.register_next_step_handler(msg, get_user_input_is_ok)
    except Exception as e:
        logger.error(e)


# 确认用户添加商品信息
def get_user_input_is_ok(message):
    try:
        if message.text.strip() == '1':
            new_comm = Commodity(chat_id=user_dict['chat_id'], title=user_dict['title'],
                                 description=user_dict['description'], price=user_dict['price'])
            session = Session()
            session.add(new_comm)
            session.commit()
            session.close()
            bot.reply_to(message, '添加成功')
        else:
            pass
    except Exception as e:
        logger.error(e)


# 我的货架
@bot.callback_query_handler(func=lambda call: call.data == 'my_shelf')
def my_shelf(call):
    try:
        session = Session()
        info = session.query(Commodity).filter(Commodity.chat_id == call.from_user.id).all()
        if len(info) > 0:
            msg = '您发布过的商品有:\n'
            for one in info:
                msg += "❤️标题: {:} - 价格: {} - 发布时间: {}\n".format(one.title, one.price, one.add_time)
            bot.send_message(call.message.chat.id, msg)
        else:
            bot.reply_to(call.message, '😂暂无商品,快去发布你的第一个商品吧~')
        session.close()
    except Exception as e:
        logger.error(e)


# 交易完成
@bot.callback_query_handler(func=lambda call: call.data == 'all_rigth')
def all_riget(call):
    try:
        session = Session()
        infos = session.query(Commodity).filter(
            and_(Commodity.chat_id == call.from_user.id, Commodity.is_over == 1)).all()
        if len(infos) > 0:
            msg = '您交易完成的商品有:\n'
            for one in infos:
                msg += "❤️标题: {:} - 价s格: {} - 交易时间: {}\n".format(one.title, one.price, one.updatetime)
            bot.send_message(call.message.chat.id, msg)
        else:
            bot.reply_to(call.message, '😂暂无商品,快去发布你的第一个商品吧~')
        session.close()
    except Exception as e:
        logger.info(e)


@bot.message_handler(func=lambda msg: msg.text == '🏧充币/提币')
def get_buyer_info(msg):
    try:
        bot.send_message(msg.chat.id, "欢迎!你的余额:0BTC\n", reply_markup=recharge_markup())
    except Exception as e:
        logger.error(e)


@bot.message_handler(func=lambda msg: msg.text == '🙋🏻‍♂️联系客服')
def get_buyer_info(msg):
    try:
        bot.send_message(msg.chat.id, "客服只负责处理交易纠纷,充提币问题以及系统错误.")
    except Exception as e:
        logger.error(e)


@bot.message_handler(func=lambda msg: msg.text)
def search_text(msg):
    try:
        info_dic = get_user_shelf_and_save(msg)
        print(info_dic)

    except:
        pass


if __name__ == '__main__':
    bot.skip_pending = True
    bot.polling(none_stop=True)
