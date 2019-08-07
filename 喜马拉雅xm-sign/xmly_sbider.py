#!/usr/bin/python3
# _*_ coding=utf-8 _*_
# @Author   :天山一枝梅
# @time     :2019/8/7 14:19
# @File     :xmly_sbider.py
# @Software :PyCharm
# 本脚本由最强网络编程大牛编写

import hashlib
import time
import random
import requests
from fake_useragent import UserAgent


# 获取喜马拉雅音频文件
def get_xmlymp3_url(url: str) -> dict:
    # 获取服务器时间，生成 xm-sign 签名
    def xm_md5() -> str:
        d = hashlib.md5()
        url = 'https://www.ximalaya.com/revision/time'
        headr = {'User-Agent': UserAgent().random,
                 'Host': 'www.ximalaya.com',
                 'Accept-Encoding': 'gzip, deflate, br'}
        res = requests.get(url, headers=headr)
        dat = 'ximalaya-' + res.text
        d.update(dat.encode('utf-8'))
        dd = d.hexdigest()
        return dd + '(' + str(random.randint(0, 100)) + ')' + res.text + '(' + str(random.randint(0, 100)) + ')' + str(
            int(time.time() * 1000))

    headers = {'xm-sign': xm_md5(),
               'User-Agent': UserAgent().random}
    return requests.get(url, headers=headers).json()


get_xmlymp3_url('https://www.ximalaya.com/revision/play/album?albumId=23467205&pageNum=1&pageSize=30')
# {'ret': 200, 'msg': '声音播放数据', 'data': {'uid': 0, 'albumId': 23467205, 'sort': 1, 'pageNum': 1, 'pageSize': 30,
#                                        'tracksAudioPlay': [
#                                            {'index': 30, 'trackId': 183340894, 'trackName': '模仿翻唱 - 姬和部濡',
#                                             'trackUrl': '/yinyue/23467205/183340894',
#                                             'trackCoverPath': '//s1.xmcdn.com/css/img/common/track_100.jpg',
#                                             'albumId': 23467205, 'albumName': '抖音最火热翻唱音乐',
#                                             'albumUrl': '/yinyue/23467205/', 'anchorId': 124342810, 'canPlay': True,
#                                             'isBaiduMusic': False, 'isPaid': False, 'duration': 248,
#                                             'src': 'https://fdfs.xmcdn.....}
