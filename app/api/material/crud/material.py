# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 10:40
# @Author  : Xiaoyunlong
from app.setting import main_init
from database.db_con import Db_Connection
import time,json,uuid
from fastapi import Header
from jose import jwt
import pandas as pd
import datetime,hashlib

config = main_init.Init_Config('81.69.29.78','cdbd','root','111')
mysql_db=Db_Connection(config.msqusername,config.msqpassword,config.msqlserver,config.msqdb,config.msqcoding)


class CRUDCategory(object):

    def get_id(self):
        try:
            all_sql = "SELECT id FROM b_data_temp"
            df = mysql_db.obtain_mysql_df(all_sql)
            return True, df
        except Exception as msg:
            return False, msg, 0

    def handle_limit_sql(self,parames: dict):
        """
        处理分页的规则
        """
        sql = f" limit {parames['pagesize'] * (parames['curpage'] - 1)},{parames['pagesize']}"
        return sql

    def add_material(self,parames: dict, ) -> bool:
        try:
            ALGORITHM = "HS256"
            token = parames["token"]
            payload = jwt.decode(
                token,
                config.SECRET_KEY, algorithms=[ALGORITHM]
            )
            userid = payload['username']
            result, df = self.get_id()
            if result and len(df) != 0:
                id = int(max(df["id"].tolist())) + 1
            else:
                id = 1
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            params = [id, parames["name"], parames["url"], userid, create_time, create_time]
            sql = 'INSERT INTO `b_data_temp`(id, name, url, user_id, create_time, update_time) VALUES (%s,%s,%s,%s,%s,%s)'
            mysql_db.commit_sql(sql, params)
            return True
        except Exception as errmsg:
            print(errmsg)
            return False

    def get_material(self,parames: dict):
        try:
            limit_sql = self.handle_limit_sql(parames)
            ALGORITHM = "HS256"
            token = parames["token"]
            payload = jwt.decode(
                token,
                config.SECRET_KEY, algorithms=[ALGORITHM]
            )
            username = payload['username']
            params1 = [username]
            sql1 = "select id from sys_user WHERE username=%s"
            df_userid = mysql_db.all(sql1, params1)
            params_rolename = [df_userid[0][0]]
            sql_role = 'SELECT sys_role.role_name from sys_role,sys_user_role WHERE sys_role.id=sys_user_role.role_id and sys_user_role.user_id=%s'
            df_role = mysql_db.all(sql_role, params_rolename)
            rolename = []
            for i in df_role:
                rolename.append(i)
            if '客户经理' in rolename:
                parms1 = [username]
                sql = "SELECT * from b_data_temp WHERE user_id=%s ORDER BY create_time DESC " + limit_sql
                sql_count = "SELECT * from b_data_temp WHERE user_id=%s"
                df = mysql_db.all(sql, parms1)
                df_count = mysql_db.all(sql_count, parms1)
                list = []
                for i in df:
                    dic = {}
                    dic['id'] = i[0]
                    dic['name'] = i[1]
                    dic['url'] = i[2]
                    dic['user_id'] = i[3]
                    dic['create_time'] = int(time.mktime(i[4].timetuple()) * 1000)
                    dic['update_time'] = int(time.mktime(i[5].timetuple()) * 1000)
                    list.append(dic)
                return True, list, len(df_count)
            else:
                sql = "SELECT * from b_data_temp ORDER BY create_time DESC " + limit_sql
                sql_count = "SELECT * from b_data_temp"
                df = mysql_db.all(sql)
                df_count = mysql_db.all(sql_count)
                list = []
                for i in df:
                    dic = {}
                    dic['id'] = i[0]
                    dic['name'] = i[1]
                    dic['url'] = i[2]
                    dic['user_id'] = i[3]
                    dic['create_time'] = int(time.mktime(i[4].timetuple()) * 1000)
                    dic['update_time'] = int(time.mktime(i[5].timetuple()) * 1000)
                    list.append(dic)
                return True, list, len(df_count)
        except Exception as msg:
            return False, msg, 0

    def update_material(self,parames: dict):
        try:
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            params = [parames["name"], parames["url"], create_time, parames["id"]]
            sql = 'UPDATE b_data_temp SET name=%s,url=%s,update_time=%s WHERE id=%s'
            mysql_db.commit_sql(sql, params)
            return True
        except Exception as msg:
            return False, msg, 0

    def delete_material(self,id):
        try:
            params = [id]
            delete_sql = "DELETE FROM `b_data_temp` WHERE id = %s"
            mysql_db.commit_sql(delete_sql, params)
            return True
        except Exception as errmsg:
            return False


curd_category = CRUDCategory()