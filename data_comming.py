# *--conding:utf-8--*
import os
from config import MUSIC_PATH
from os import rename
import youtube_dl


def get_username_from_message(message):
    if message.from_user.username:
        return message.from_user.username
    else:
        return ''


def get_nickname_from_message(message):
    frist_name = message.from_user.first_name
    last_name = message.from_user.last_name
    if frist_name and last_name and frist_name != last_name:
        username = frist_name + last_name
    else:
        username = frist_name
    return username


def get_chat_id_from_message(message):
    return message.from_user.id


def get_all_music_list():
    return [i for root, dirs, files in os.walk(MUSIC_PATH, ) for i in files if
            i and os.path.splitext(i)[1].lower() == '.m4a' or os.path.splitext(i)[1].lower() == '.mp3']


def download(youtube_url, name):
    """
    download the video from the given url
    """

    def rename_hook(d):
        """
        youtube-dl's hook to rename the downloaded video name
        """

        if d['status'] == 'finished':
            file_name = name + '.mp3'
            rename(d['filename'], file_name)

    # 定义某些下载参数
    ydl_opts = {
        # 'format': 'bestaudio/best',
        'progress_hooks': [rename_hook],
        # outtmpl 格式化下载后的文件名，避免默认文件名太长无法保存
        'outtmpl': '%(id)s%(ext)s'
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
