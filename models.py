# *--conding:utf-8--*
import time

from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///telegram.db?check_same_thread=False', echo=True, encoding='utf-8')
Base = declarative_base()

Session = sessionmaker(bind=engine)


class Music(Base):
    """用户表"""
    __tablename__ = 'music'
    id = Column(Integer, primary_key=True, unique=True)
    title = Column(String(20), comment='音乐名')
    url = Column(String(50), comment='播放链接')
    singer = Column(String(10), default='', comment='歌手')
    song_type = Column(String(20), comment='所属类型')
    is_hot = Column(Integer, default=0, comment='是否推荐')
    createtime = Column(DateTime(), server_default=func.now(), comment='添加时间')

    def __repr__(self):
        return "<User(title='%s', url='%s', singer='%s',song_type='%s',is_hot='%d')>" % (
            self.title, self.url, self.singer, self.song_type, self.is_hot)


# 精确搜索
def search_db(name):
    session = Session()
    result = session.query(Music.title, Music.url).filter(Music.title.like('%' + name + '%')).one()
    session.close()
    return result


# 查找推荐
def search_db_by_hot(num: int):
    session = Session()
    result = session.query(Music.title, Music.url).filter(Music.is_hot == num).all()
    session.close()
    return result


# 类型查找
def search_db_by_type(type):
    session = Session()
    result = session.query(Music.title, Music.url).filter(Music.song_type == type).all()
    session.close()
    return result


