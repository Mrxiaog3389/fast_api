# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 10:40
# @Author  : Xiaoyunlong
import os,time,logging
from app.setting import main_init
from logging.handlers import RotatingFileHandler

config = main_init.Init_Config('192.168.4.131','app.exam','root','123456!@#')

# 定位到log日志文件
log_path = os.path.join(config.BASE_DIR, 'logs')
if not os.path.exists(log_path):
    os.mkdir(log_path)
log_path_error = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_error.log')
log_path_info = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_info.log')

#需修改时，注意日志路径
#基础日志
logging.basicConfig(level = logging.INFO,
                    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S, %a',
                    filename=log_path_info,
                    filemode='a')


#调试窗口显示
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

#报错的日志
#定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
file_log_handler = RotatingFileHandler(log_path_error, maxBytes=1024*1024*100, backupCount=10)
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
file_log_handler.setFormatter(formatter)
logging.getLogger().addHandler(file_log_handler)
logging.basicConfig(level=logging.DEBUG)