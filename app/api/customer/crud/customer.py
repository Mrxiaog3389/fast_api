# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 10:40
# @Author  : Xiaoyunlong
from app.setting import main_init
from database.db_con import Db_Connection
import time,json,uuid
from fastapi import Header
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

    def add_customer(self,parames: dict) -> bool:
        try:
            user_id = str(uuid.uuid4())
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            id = str(uuid.uuid1())
            role_id = '2'
            params = [id, user_id, parames["cust_name"], parames["org_name"], parames["tel"], parames["phone"],
                      parames["company"], parames["job_number"], parames["profile"], parames["image"], create_time]
            sql = 'INSERT INTO `b_customer_manager`(id, user_id, cust_name, org_name, tel, phone, company,job_number,profile,image,create_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            params1 = [user_id, role_id]
            sql1 = 'INSERT INTO sys_user_role(user_id,role_id) VALUES (%s,%s)'
            password = '123456'
            bytes_url = hashlib.md5(password.encode())
            hashed = bytes_url.hexdigest()
            openid = ''
            params2 = [user_id, parames["phone"], hashed, openid, parames["job_number"], parames["image"], create_time]
            sql2 = 'INSERT INTO sys_user(id,username,password,openid,nick_name,face_img,create_time) VALUES (%s,%s,%s,%s,%s,%s,%s)'
            mysql_db.commit_sql(sql, params)
            mysql_db.commit_sql(sql1, params1)
            mysql_db.commit_sql(sql2, params2)
            return True
        except Exception as errmsg:
            return False

    def get_customer(self,parames: dict):
        try:
            limit_sql = self.handle_limit_sql(parames)
            all_sql = "SELECT * FROM b_customer_manager ORDER BY create_time DESC" + limit_sql
            all_customer_sql = "SELECT * FROM b_customer WHERE user_id=%s"
            all_count_sql = "SELECT * FROM b_customer_manager"
            df = mysql_db.all(all_sql)
            list = []
            for i in df:
                Dic = {}
                Dic['id'] = i[0]
                Dic['user_id'] = i[1]
                Dic['cust_name'] = i[2]
                Dic['org_name'] = i[3]
                Dic['tel'] = i[4]
                Dic['phone'] = i[5]
                Dic['company'] = i[6]
                Dic['job_number'] = i[7]
                Dic['profile'] = i[8]
                Dic['image'] = i[9]
                Dic['create_time'] = int(time.mktime(i[10].timetuple()) * 1000)
                Dic['resourceList'] = []
                df_customer = mysql_db.all(all_customer_sql, i[1])
                for j in df_customer:
                    dic = {}
                    dic['id'] = j[0]
                    dic['cust_name'] = j[2]
                    dic['phone'] = j[3]
                    dic['company'] = j[4]
                    dic['address'] = j[5]
                    dic['create_time'] = j[6]
                    dic['openid'] = j[7]
                    Dic['resourceList'].append(dic)
                list.append(Dic)
            df_count = mysql_db.all(all_count_sql)

            return True, list, len(df_count)
        except Exception as msg:
            return False, msg, 0

    def update_customer(self,parames: dict):
        try:
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            params = [parames["cust_name"], parames["org_name"], parames["tel"], parames["phone"], parames["company"],
                      parames["job_number"], parames["profile"], parames["image"], create_time, parames["id"]]
            sql = 'UPDATE b_customer_manager SET cust_name=%s,org_name=%s,tel=%s,phone=%s,company=%s,job_number=%s,profile=%s,image=%s,create_time=%s WHERE id =%s'
            parms3 = [parames["id"]]
            sql8 = "SELECT user_id FROM b_customer_manager WHERE id=%s"
            df = mysql_db.all(sql8, parms3)
            params1 = [parames["image"], create_time, parames["phone"], parames["job_number"], df[0][0]]
            sql4 = 'UPDATE sys_user SET face_img=%s,update_time=%s,username=%s,nick_name=%s WHERE id =%s'
            mysql_db.commit_sql(sql, params)
            mysql_db.commit_sql(sql4, params1)
            return True
        except Exception as msg:
            return False, msg, 0

    def delete_customer(self,parames: dict):
        try:
            for li in parames["lists"]:
                parms = [li]
                sql2 = "SELECT user_id FROM b_customer_manager WHERE id=%s"
                df = mysql_db.all(sql2, parms)
                params = [li]
                params1 = [df[0][0]]
                sql = 'DELETE FROM `b_customer_manager` WHERE id = %s'
                sql1 = 'DELETE FROM `sys_user_role` WHERE user_id = %s'
                sql3 = 'DELETE FROM `sys_user` WHERE id = %s'
                mysql_db.commit_sql(sql, params)
                mysql_db.commit_sql(sql1, params1)
                mysql_db.commit_sql(sql3, params1)
            return True
        except Exception as errmsg:
            return False


curd_category = CRUDCategory()