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

    def handle_limit_sql(self,parames: dict):
        """
        处理分页的规则
        """
        sql = f" limit {parames['pagesize'] * (parames['curpage'] - 1)},{parames['pagesize']}"
        return sql

    def get_id_order_no(self):
        try:
            all_sql = "SELECT * from b_message_notification ORDER BY create_time DESC "
            df = mysql_db.obtain_mysql_df(all_sql)
            return True, df
        except Exception as msg:
            return False, msg, 0

    def add_message(self,parames: dict) -> bool:
        try:
            result, df = self.get_id_order_no()
            if result and len(df) != 0:
                order_no = max(df["order_no"].tolist()) + 1
            else:
                order_no = 1
            ALGORITHM = "HS256"
            token = parames["token"]
            payload = jwt.decode(
                token,
                config.SECRET_KEY, algorithms=[ALGORITHM]
            )
            create_user_name = payload['username']
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            id = str(uuid.uuid1())
            params = [id, parames["title"], parames["remark"], parames["content"], parames["url"], order_no,create_user_name, parames["object"], create_time]
            sql = 'INSERT INTO `b_message_notification`(id, title, remark, content, url, order_no, create_user_name,object,create_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql_db.commit_sql(sql, params)
            return True
        except Exception as errmsg:
            return False

    def get_message(self,parames: dict):
        try:
            limit_sql = self.handle_limit_sql(parames)
            all_sql = "SELECT * from b_message_notification ORDER BY create_time DESC " + limit_sql
            all_count_sql = "SELECT * from b_message_notification"
            df = mysql_db.all(all_sql)
            list = []
            for i in df:
                dic = {}
                dic['content'] = i[3]
                dic['createTime'] = int(time.mktime(i[8].timetuple()) * 1000)
                dic['createUserName'] = i[6]
                dic['id'] = i[0]
                dic['orderNo'] = i[5]
                dic['remark'] = i[2]
                dic['title'] = i[1]
                dic['url'] = i[4]
                if i[7] == 1:
                    dic['object'] = '客户'
                else:
                    dic['object'] = '客户经理'
                list.append(dic)
            df_count = mysql_db.all(all_count_sql)
            return True, list, len(df_count)
        except Exception as msg:
            return False, msg, 0

    def update_message(self,parames: dict):
        try:
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            params = [parames["title"], parames["remark"], parames["content"], parames["url"], create_time,
                      parames["object"], parames["id"]]
            print(params)
            sql = 'UPDATE b_message_notification SET title=%s,remark=%s,content=%s,url=%s,create_time=%s,object=%s WHERE id=%s'
            mysql_db.commit_sql(sql, params)
            return True
        except Exception as msg:
            return False, msg, 0

    def delete_message(self,parames: dict):
        try:
            for li in parames["lists"]:
                params = [li]
                delete_sql = "DELETE FROM `b_message_notification` WHERE id = %s"
                mysql_db.commit_sql(delete_sql, params)
            return True
        except Exception as errmsg:
            return False


curd_category = CRUDCategory()