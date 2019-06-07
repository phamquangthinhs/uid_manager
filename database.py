# -*- coding: utf-8 -*-
import re, ast, json, requests
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import datetime

db_name = 'master.db'
engine = create_engine('sqlite:///module/{}?check_same_thread=False'.format(db_name))
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

token = 'EAACW5Fg5N2IBAPMGoJDi3OdZBzw5RtvJ0FovwyIFH3BAmxgpNPU0LBkBpzWtE58VGrSFpyA9AeOHvrZC8i8MT8yNOcFWubajuEl3NGs5LDqh8B2CXx1pZCLhqV5ZAfXZBDG0uj8vDe6uDtq5OGqLDJMnpuEZBC3V0ZB8vPaiVokR6I7G9RuAZAsJ8Kzkzfp6yC4ZD'

class uid_manager(Base):
    __tablename__ = 'uid_facebook'

    id = Column(Integer, primary_key=True)
    uid = Column(String(50))

    def add_uid(self, uid):
        session.add(uid_manager(uid=uid))
        session.commit()
    def query_uid(self, id):
        return session.query(uid_manager).filter(uid_manager.id == id).first()
    def del_uid(self, uid):
    	data = session.query(uid_manager).filter(uid_manager.uid == uid).first()
        session.delete(data)
        session.commit()
    def del_all(self):
        data = session.query(uid_manager).delete()
        session.commit()
    def max_uid(self):
        return session.query(func.max(uid_manager.id)).one()
    def min_uid(self):
        return session.query(func.min(uid_manager.id)).one()

class acc_manager(Base):
    __tablename__ = 'cookies_fb'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    uid = Column(String(50))
    cookies = Column(String(50))
    last_activate = Column(String(50))

    def add_cookies(self, name, uid, cookies):
        session.add(acc_manager(name=name, uid=uid, cookies=cookies))
        session.commit()
    def query_all(self):
        return session.query(acc_manager).all()
    def del_cookies(self, uid):
        data = session.query(acc_manager).filter(acc_manager.uid == uid).first()
        session.delete(data)
        session.commit()
    def yes_itlive(self, uid, time):
        nick = session.query(acc_manager).filter(acc_manager.uid == uid).first()
        nick.last_activate = time
        session.commit()
    def query_cookies(self, uid):
        return session.query(acc_manager).filter(acc_manager.uid == uid).first()
    def what_last(self, uid):
        nick = session.query(acc_manager).filter(acc_manager.uid == uid).first()
        return nick.last_activate

# Database Control
def db_master(**kwargs):
    db_control = {}

    for key, value in kwargs.items():
        db_control[key] = value
    if db_control['mode'] == 'add_uid':
        uid_manager().add_uid(db_control['uid'])
    if db_control['mode'] == 'del_all':
        uid_manager().del_all()
    if db_control['mode'] == 'max_uid':
        return uid_manager().max_uid()[0]
    if db_control['mode'] == 'min_uid':
        return uid_manager().min_uid()[0]
    if db_control['mode'] == 'query_uid':
        return uid_manager().query_uid(db_control['idx'])
    if db_control['mode'] == 'del_uid':
        uid_manager().del_uid(db_control['uid'])
    if db_control['mode'] == 'get_uid':
        return get_uid()
    if db_control['mode'] == 'add_cookies':
        read_cookies(db_control['cookies'])
    if db_control['mode'] == 'qall_cookies':
        return acc_manager().query_all()
    if db_control['mode'] == 'del_cookies':
        acc_manager().del_cookies(db_control['uid'])
    if db_control['mode'] == 'live_cookies':
        acc_manager().yes_itlive(db_control['uid'], db_control['time'])
    if db_control['mode'] == 'query_cookies':
        return acc_manager().query_cookies(db_control['uid'])
    if db_control['mode'] == 'die_check':
        a = acc_manager().what_last(db_control['uid'])
        return ss_time(a)

# Get & Del Uid
def get_uid():
    i = db_master(mode='min_uid')
    a = db_master(mode='query_uid', idx = i)
    b = a.uid
    db_master (mode='del_uid', uid = b)
    return b

# Read cookies Facebook
def read_cookies(cookie):
    c = json.loads(cookie)
    c = c[1]
    d = c['value']
    response = requests.get('https://graph.facebook.com/{}?fields=id,name&access_token={}'.format(d,token))
    e = json.loads(response.content)
    acc_manager().add_cookies(name=e['name'], uid=e['id'], cookies=cookie)

# Read Time
def return_time(str_time):
    a = u''.join(str_time).encode('utf-8').strip()
    a = a.split()[-1]
    a = a.split(":")
    return datetime.time(int(a[0]),int(a[1]),int(a[2]))

def return_date(str_time):
    a = u''.join(str_time).encode('utf-8').strip()
    a = a.split()[0]
    a = a.split("/")
    return datetime.date(1,int(a[0]),int(a[1]))

def ss_date(date):
    now = datetime.datetime.now()
    b = now.strftime("%d/%m %H:%M:%S")
    a, b = return_date(date),return_date(b)
    print (a)
    print (b)
    if a < b:
        print ('False')
    if a == b:
        print ('True')

def ss_time(time): 
    now = datetime.datetime.now()
    b = now.strftime("%d/%m %H:%M:%S")
    a, b = return_time(time), return_time(b)
    c = (datetime.datetime.combine(datetime.date(1, 1, 1), a) + datetime.timedelta(minutes=15)).time()
    if c > b:
        return True
    if c < b:
        return False

if __name__ == '__main__':
    pass
    # 100032075779910
    a = acc_manager().what_last('100032075779910')
    ss_date(a)

    
    

