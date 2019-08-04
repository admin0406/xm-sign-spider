# *--conding:utf-8--*
import time

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

__all__ = (['Session', 'User', 'Record', 'Commodity'])

engine = create_engine('sqlite:///telegram.db?check_same_thread=False', echo=True, encoding='utf-8')
Base = declarative_base()


Session = sessionmaker(bind=engine)


class User(Base):
    """用户表"""
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True, unique=True)
    chat_id = Column(Integer, comment='用户唯一id')
    user_key = Column(String(100), comment='用户密匙')
    coin = Column(Integer, default=0, comment='用户余额')
    fcoin = Column(Integer, default=0, comment='冻结资金')
    my_shelf = Column(String(100000), comment='我的购物车')
    createtime = Column(DateTime(), server_default=func.now(), comment='创建时间')
    updatetime = Column(DateTime(), server_default=func.now(), onupdate=func.now(), comment='修改时间')

    def __repr__(self):
        return "<User(chat_id='%d', user_key='%s', coin='%d',fcoin='%d',my_shelf='%s')>" % (
            self.chat_id, self.user_key, self.coin, self.fcoin, self.my_shelf)


class Record(Base):
    """交易记录表"""
    __tablename__ = 'members_record'
    id = Column(Integer, primary_key=True, unique=True)
    chat_id = Column(Integer, comment='用户唯一id')
    trans_amount = Column(Integer, comment='交易金额')
    order_id = Column(Integer, comment='订单号')
    over_coin = Column(Integer, comment='交易后资金余额')
    createtime = Column(DateTime(), server_default=func.now(), comment='交易时间')

    def __repr__(self):
        return "<Record(chat_id='%d', trans_amount='%d', order_id='%d',over_coin='%d')>" % (
            self.chat_id, self.trans_amount, self.order_id, self.over_coin)


class Commodity(Base):
    """商品表"""
    __tablename__ = 'commodity'
    id = Column(Integer, primary_key=True, unique=True)
    chat_id = Column(Integer, comment='用户唯一id')
    title = Column(String, comment='商品标题')
    description = Column(String, comment='商品描述')
    price = Column(Integer, comment='商品价格')
    is_over = Column(Integer, default=0, comment='是否已经交易')
    add_time = Column(DateTime(), server_default=func.now(), comment='创建时间')
    updatetime = Column(DateTime(), server_default=func.now(), onupdate=func.now(), comment='修改时间')
    def __repr__(self):
        return "<User(chat_id='%d', title='%s', description='%s',price='%d',is_over='%s')>" % (
            self.chat_id, self.title, self.description, self.price, self.is_over)

Base.metadata.create_all(engine)