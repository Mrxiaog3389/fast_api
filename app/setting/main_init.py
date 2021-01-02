# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 10:40
# @Author  : Xiaoyunlong
import jwt,time
import configparser
import os,sys
import logging
import redis

def read_config(ip,database,username,password):
    """
    读取配置
    :return: 返回配置对象
    """
    config = configparser.ConfigParser()  # 类实例化
    ini_path = os.getcwd() + '\\config.ini'
    config.read(ini_path)
    config.add_section('mysqldb')
    config.set('mysqldb','msqlserver',ip)
    config.set('mysqldb', 'msqdb', database)#database
    config.set('mysqldb', 'msqusername', username)
    config.set('mysqldb', 'msqpassword', password)
    config.set('mysqldb', 'msqcoding', 'utf8')
    config.add_section('redis')
    config.set('redis', 'REDIS_HOST', '127.0.0.1')
    config.set('redis', 'REDIS_PORT', '6379')
    config.set('redis', 'REDIS_PASSWORD', 'root12345')
    config.set('redis', 'REDIS_DB', '0')
    config.add_section('flask-session')
    config.set('flask-session', 'SESSION_TYPE', 'redis')
    config.set('flask-session', 'PERMANENT_SESSION_LIFETIME', '86400')
    config.add_section('token')
    config.set('token', 'SECRET_KEY', r'\x88D\xf09\x6\xa0A\x7\xc5V\xbe\x8b\xef\xd7\xd8\xd3\xe6\x98*4')
    config.set('token', 'SECRET', "zhananbudanchou1234678")
    config.set('token', 'USER_SECRET', 'wasrdfgjhkhgfdsa')
    config.set('token', 'USER_NAME', "DAFAGADAWD")
    return config

class Init_Config(object):
    """
    初始化配置
    """
    def __init__(self,ip,database,username,password):
        sys.path.append(os.getcwd())
        config = read_config(ip,database,username,password)
        # mysql 配置
        self.msqlserver = config['mysqldb']['msqlserver']
        self.msqdb = config['mysqldb']['msqdb']
        self.msqusername = config['mysqldb']['msqusername']
        self.msqpassword = config['mysqldb']['msqpassword']
        self.msqcoding = config['mysqldb']['msqcoding']

        # redis配置
        self.rediserver = config['redis']['REDIS_HOST']
        self.redispassword=config['redis']['REDIS_PASSWORD']
        self.rediport = config['redis']['REDIS_PORT']
        self.redidb = config['redis']['REDIS_DB']
        self.rediurl :str = f"redis://:{self.redispassword}@{self.rediserver}:{self.rediport}/{self.redidb}?encoding=utf-8"

        self.SESSION_TYPE = config['flask-session']['SESSION_TYPE']
        self.SESSION_USE_SIGNER = True
        self.PERMANENT_SESSION_LIFETIME = config['flask-session']['PERMANENT_SESSION_LIFETIME']
        self.SESSION_REDIS = redis.StrictRedis(host=self.rediserver, port=self.rediport)

        # jwt加密算法
        self.JWT_ALGORITHM: str = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES :int=  24 * 3600
        self.SECRET_KEY = config['token']['SECRET_KEY']
        self.SECRET = config['token']['SECRET']
        self.USER_SECRET = config['token']['USER_SECRET']
        self.USER_NAME = config['token']['USER_NAME']

        # 根路径
        self.BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
