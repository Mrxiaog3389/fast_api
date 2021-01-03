# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 10:40
# @Author  : Xiaoyunlong
from app.setting import main_init
from database.db_con import Db_Connection
from jose import jwt
import calendar

config = main_init.Init_Config('81.69.29.78','cdbd','root','111')
mysql_db=Db_Connection(config.msqusername,config.msqpassword,config.msqlserver,config.msqdb,config.msqcoding)


class CRUDCategory(object):

    def analysis(self,parames: dict):
        username = parames["token"]['username']
        params1 = [username]
        sql1 = "select id from sys_user WHERE username=%s"
        df_userid = mysql_db.all(sql1, params1)
        params_rolename = [df_userid[0][0]]
        sql_role = 'SELECT sys_role.role_name from sys_role,sys_user_role WHERE sys_role.id=sys_user_role.role_id and sys_user_role.user_id=%s'
        df_role = mysql_db.all(sql_role, params_rolename)
        rolename = []
        for i in df_role:
            rolename.append(i[0])
        if '客户经理' in rolename:
            sql4 = "SELECT id FROM b_customer_manager WHERE user_id=%s"
            df_customerid = mysql_db.all(sql4, params_rolename)

            list = []
            parms3 = [df_customerid[0][0]]
            sql6 = "SELECT COUNT(*) from b_job,b_job_flow WHERE b_job.pro_no=b_job_flow.job_id AND manager_id=%s AND b_job_flow.status>3 GROUP BY b_job.create_time"
            sql7 = mysql_db.all(sql6, parms3)
            dic3 = {}
            dic3['title'] = '已办'
            if len(sql7) == 0:
                dic3['values'] = 0
            else:
                dic3['values'] = sql7[0][0]
            list.append(dic3)

            parms4 = [df_customerid[0][0]]
            sql10 = "SELECT COUNT(*) from b_job,b_job_flow WHERE b_job.pro_no=b_job_flow.job_id AND manager_id=%s AND (b_job_flow.status=1 or b_job_flow.status=4) GROUP BY b_job.create_time"
            sql11 = mysql_db.all(sql10, parms4)
            dic4 = {}
            dic4['title'] = '待办'
            if len(sql11) == 0:
                dic4['values'] = 0
            else:
                dic4['values'] = sql11[0][0]
            list.append(dic4)
            return list
        else:
            managerList = []
            sql18 = "SELECT COUNT(1) AS total, DATE_FORMAT(b_job.create_time,'%Y-%m-%d') AS days from b_job,b_job_flow WHERE b_job.pro_no=b_job_flow.job_id AND b_job_flow.status>3 GROUP BY days ORDER BY days DESC;"
            sql19 = mysql_db.all(sql18)
            dic = {}
            dic['title'] = '已办'
            if len(sql19) == 0:
                dic['values'] = 0
            else:
                dic['values'] = sql19[0][0]
            managerList.append(dic)
            sql20 = "SELECT COUNT(1) AS total, DATE_FORMAT(b_job.create_time,'%Y-%m-%d') AS days from b_job,b_job_flow WHERE b_job.pro_no=b_job_flow.job_id AND (b_job_flow.status=1 or b_job_flow.status=4) GROUP BY days ORDER BY days DESC;"
            sql21 = mysql_db.all(sql20)
            dic1 = {}
            dic1['title'] = '待办'
            if len(sql21) == 0:
                dic1['values'] = 0
            else:
                dic1['values'] = sql21[0][0]
                managerList.append(dic1)
            return managerList

    def year(self,parames: dict):
        username = parames["token"]['username']
        params1 = [username]
        sql1 = "select id from sys_user WHERE username=%s"
        df_userid = mysql_db.all(sql1, params1)
        params_rolename = [df_userid[0][0]]
        sql_role = 'SELECT sys_role.role_name from sys_role,sys_user_role WHERE sys_role.id=sys_user_role.role_id and sys_user_role.user_id=%s'
        df_role = mysql_db.all(sql_role, params_rolename)
        rolename = []
        for i in df_role:
            rolename.append(i[0])

        list = []
        if '客户经理' in rolename:
            parms5 = [df_userid[0][0]]
            sql4 = "SELECT id FROM b_customer_manager WHERE user_id=%s"
            sql5 = mysql_db.all(sql4, parms5)
            sql6 = "SELECT COUNT(*),b_job.create_time from b_job,b_job_flow WHERE b_job.pro_no=b_job_flow.job_id AND b_job_flow.status>3 AND day(b_job.create_time)=%s AND year(b_job.create_time)=%s AND month(b_job.create_time)=%s AND manager_id=%s GROUP BY b_job.create_time"
            now = calendar.monthrange(parames['year'], (parames['month']))
            for d in range(1, now[1] + 1):
                dic = {}
                dic['day'] = d
                parms3 = [d, parames['year'], parames['month'],sql5[0][0]]
                sql7 = mysql_db.all(sql6, parms3)
                if len(sql7) == 0:
                    dic['value'] = 0
                else:
                    dic['value'] = sql7[0][0]
                list.append(dic)
            return list

        else:
            sql6 = "SELECT COUNT(*),b_job.create_time from b_job,b_job_flow WHERE b_job.pro_no=b_job_flow.job_id AND b_job_flow.status>3 AND day(b_job.create_time)=%s AND year(b_job.create_time)=%s AND month(b_job.create_time)=%s GROUP BY b_job.create_time"
            now = calendar.monthrange(parames['year'], (parames['month']))
            for d in range(1, now[1] + 1):
                dic = {}
                dic['day'] = d
                parms3 = [d,parames['year'], parames['month']]
                sql7 = mysql_db.all(sql6, parms3)
                if len(sql7) == 0:
                    dic['value'] = 0
                else:
                    dic['value'] = sql7[0][0]
                list.append(dic)
            return list



curd_category = CRUDCategory()