# *--conding:utf-8--*
import os
API_TOKEN = '938619629:AAF3aR9AQniQzHJSb3PJChocfBnlKMLQiqs'
black_path = 'black_path'
admin_path = 'admin_list'
address_path = 'address'

# 日志配置

LOG = {
    'file_name': 'telegram_bot.log',
    'backup': 5,
    'console_level': 'INFO',
    'file_level': 'DEBUG',
    'pattern': ''
}

# 三方api接入
URL = {
    # 笑话
    'joke_url': 'http://www.mxnzp.com/api/jokes/list/random',
    # 新闻
    'news_list': 'http://www.mxnzp.com/api/news/list?typeId=525&page=1',
    # 请求新闻
    'news_details': 'http://www.mxnzp.com/api/news/details',
    # 天气
    'weather_url': 'http://www.mxnzp.com/api/weather/current/深圳市'
}

