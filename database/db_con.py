# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 10:40
# @Author  : Xiaoyunlong
from app.setting import main_init
from sqlalchemy import create_engine
from app.common.logger import *
import pandas as pd
from re import sub
import pymysql

class Db_Connection(object):
    def __init__(self,msqusername,msqpassword,msqlserver,msqdb,msqcoding):
        self.msqusername=msqusername
        self.msqpassword = msqpassword
        self.msqlserver = msqlserver
        self.msqdb = msqdb
        self.msqcoding = msqcoding
        self.mqlengine = create_engine(
            f"mysql+pymysql://{self.msqusername}:{self.msqpassword}@{self.msqlserver}/{self.msqdb}",
            encoding=msqcoding)
        # 数据库连接状态，0为未连接，1为已连接
        self.status = 0

    def obtain_mysql_df(self, sql):
        try:
            df = pd.read_sql(sql, self.mqlengine)
            return df
        except Exception as eromsg:
            logging.error('数据库连接失败.\n\tERROR:' + str(eromsg))

    def pamras_mysql_df(self, sql,pamras):
        try:
            df = pd.read_sql(sql, self.mqlengine,params=pamras)
            return df
        except Exception as eromsg:
            logging.error('数据库连接失败.\n\tERROR:' + str(eromsg))


    def obtain_mysql_count(self, sql):
        try:
            df = pd.read_sql(sql, self.mqlengine)
            return list(df['COUNT(*)'])[0]
        except Exception as eromsg:
            logging.error('数据库连接失败.\n\tERROR:' + str(eromsg))


    def mysql_to_sql(self, df, table):
        df.to_sql(table, con=self.mqlengine, index=False, if_exists='append')

    def commit_sql(self, sql,pamres=None):
        try:
            conn = pymysql.connect(host=self.msqlserver,
                                   user=self.msqusername,
                                   password=self.msqpassword,
                                   db=self.msqdb,
                                   # charset=config.msqcoding,
                                   )
            cursor = conn.cursor()
            cursor.execute(sql,pamres)
            conn.commit()
            logging.info('SQL执行成功:' + sql)
            cursor.close()
            conn.close()
            logging.info('数据库关闭成功.')
            return True
        except Exception as eromsg:
            logging.error('数据库连接失败.\n\tERROR:' + str(eromsg))
            return False

    def all(self, sql,params=None):
        try:
            conn = pymysql.connect(host=self.msqlserver,
                                   user=self.msqusername,
                                   password=self.msqpassword,
                                   db=self.msqdb,
                                   # charset=config.msqcoding
                                   )
            cursor = conn.cursor()
            cursor.execute(sql,params)
            result =cursor.fetchall()
            logging.info('SQL执行成功:' + sql)
            cursor.close()
            conn.close()
            logging.info('数据库关闭成功.')
            return result
        except Exception as eromsg:
            print(eromsg)
            logging.error('数据库连接失败.\n\tERROR:' + str(eromsg))
