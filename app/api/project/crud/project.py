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

    def prosess_select(self,parames: dict):
        try:
            sql = "SELECT * from b_job_flow WHERE job_flow<=4 AND job_flow=%s AND job_id=%s"
            sql1 = "SELECT * from b_job_flow WHERE job_flow<=4 AND status>=4 AND job_flow=%s AND job_id=%s"
            list = ['first', 'secnrd', 'third', 'four']
            Dic = {}
            for i in range(len(list) - 3, len(list) + 1):
                if i < 4:
                    parms = [i, parames['prono']]
                    df = mysql_db.all(sql, parms)
                    for s1 in df:
                        dic = {}
                        dic['job_flow'] = s1[2]
                        dic['status'] = s1[3]
                        dic['execut_time'] = int(time.mktime(s1[6].timetuple()) * 1000)
                        dic['next_flow'] = s1[7]
                        Dic[list[i - 1]] = dic
                else:
                    parms = [i, parames['prono']]
                    df = mysql_db.all(sql1, parms)
                    for s1 in df:
                        dic = {}
                        dic['job_flow'] = s1[2]
                        dic['status'] = s1[3]
                        dic['execut_time'] = int(time.mktime(s1[6].timetuple()) * 1000)
                        dic['next_flow'] = s1[7]
                        Dic[list[i - 1]] = dic
            return True, Dic
        except Exception as msg:
            return False, msg, 0

    def project_select(self,parames: dict):
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
        sql_job1 = "SELECT * from b_job_flow WHERE job_flow>=4 AND status>=4"
        df_job1 = mysql_db.obtain_mysql_df(sql_job1)
        prono1 = df_job1['job_id'].tolist()

        sql_job = "SELECT * from b_job_flow WHERE job_flow<4 AND status<4"
        df_job = mysql_db.obtain_mysql_df(sql_job)
        prono = df_job['job_id'].tolist()
        prono_list=[]
        for p2 in prono:
            if p2 in prono1:
                continue
            prono_list.append(p2)

        if '客户经理' in rolename:
            if parames['status']==1:
                try:
                    sql = "SELECT * from b_job WHERE manager_id=%s AND pro_no=%s ORDER BY create_time ASC "
                    df_list=[]
                    for p in prono1:
                        pamra=[df_userid[0][0],p]
                        df=mysql_db.all(sql,pamra)
                        if len(df)==0:
                            continue
                        df_list.append(df[0])
                    list = []
                    for i in df_list:
                        dic = {}
                        dic['pro_no'] = i[0]
                        dic['username'] = i[1]
                        dic['project_name'] = i[2]
                        dic['address'] = i[3]
                        dic['capacity'] = float(i[4])
                        params1 = [i[5]]
                        sql14 = "SELECT cust_name FROM b_customer_manager WHERE user_id=%s"
                        sql15 = mysql_db.all(sql14, params1)
                        dic['manager_id'] = sql15[0][0]
                        dic['cust_contact'] = i[6]
                        dic['cust_phone'] = i[7]
                        dic['cust_company_name'] = i[8]
                        dic['manager_pro_url'] = i[9]
                        dic['cust_pro_url'] = i[10]
                        dic['org_name'] = i[11]
                        dic['org_qualification'] = i[12]
                        dic['img_checker'] = i[13]
                        dic['checker_phone'] = i[14]
                        dic['refuse_reason'] = i[15]
                        dic['create_time'] = int(time.mktime(i[17].timetuple()) * 1000)
                        list.append(dic)
                    return True,list,len(df_list)
                except Exception as msg:
                    return False, msg, 0
            else:
                try:
                    prono_list = set(prono_list)
                    sql = "SELECT * from b_job WHERE manager_id=%s AND pro_no=%s ORDER BY create_time ASC"
                    df_list=[]
                    for p in prono_list:
                        pamra=[df_userid[0][0],p]
                        df=mysql_db.all(sql,pamra)
                        if len(df)==0:
                            continue
                        df_list.append(df[0])
                    df_list=set(df_list)
                    list = []
                    for i in df_list:
                        dic = {}
                        dic['pro_no'] = i[0]
                        dic['username'] = i[1]
                        dic['project_name'] = i[2]
                        dic['address'] = i[3]
                        dic['capacity'] = float(i[4])
                        params1 = [i[5]]
                        sql14 = "SELECT cust_name FROM b_customer_manager WHERE user_id=%s"
                        sql15 = mysql_db.all(sql14, params1)
                        dic['manager_id'] = sql15[0][0]
                        dic['cust_contact'] = i[6]
                        dic['cust_phone'] = i[7]
                        dic['cust_company_name'] = i[8]
                        dic['manager_pro_url'] = i[9]
                        dic['cust_pro_url'] = i[10]
                        dic['org_name'] = i[11]
                        dic['org_qualification'] = i[12]
                        dic['img_checker'] = i[13]
                        dic['checker_phone'] = i[14]
                        dic['refuse_reason'] = i[15]
                        dic['create_time'] = int(time.mktime(i[17].timetuple()) * 1000)
                        list.append(dic)
                    return True,list,len(df_list)
                except Exception as msg:
                    return False, msg, 0
        else:
            if parames['status']==1:
                try:
                    prono1=set(prono1)
                    sql = "SELECT * from b_job WHERE pro_no=%s ORDER BY create_time ASC "
                    df_list = []
                    for p in prono1:
                        pamra = [p]
                        df = mysql_db.all(sql, pamra)
                        if len(df)==0:
                            continue
                        df_list.append(df[0])

                    list = []
                    for i in df_list:
                        dic = {}
                        dic['pro_no'] = i[0]
                        dic['username'] = i[1]
                        dic['project_name'] = i[2]
                        dic['address'] = i[3]
                        dic['capacity'] = float(i[4])
                        params1 = [i[5]]
                        sql14 = "SELECT cust_name FROM b_customer_manager WHERE user_id=%s"
                        sql15 = mysql_db.all(sql14, params1)
                        if len(sql15)==0:
                            dic['manager_id'] = 0
                        else:
                            dic['manager_id'] = sql15[0][0]
                        dic['cust_contact'] = i[6]
                        dic['cust_phone'] = i[7]
                        dic['cust_company_name'] = i[8]
                        dic['manager_pro_url'] = i[9]
                        dic['cust_pro_url'] = i[10]
                        dic['org_name'] = i[11]
                        dic['org_qualification'] = i[12]
                        dic['img_checker'] = i[13]
                        dic['checker_phone'] = i[14]
                        dic['refuse_reason'] = i[15]
                        dic['create_time'] = int(time.mktime(i[17].timetuple()) * 1000)
                        list.append(dic)
                    return True, list, len(df_list)
                except Exception as msg:
                    return False, msg, 0
            else:
                try:

                    prono_list=set(prono_list)
                    sql = "SELECT * from b_job WHERE pro_no=%s ORDER BY create_time ASC "
                    df_list = []
                    for p in prono_list:
                        pamra = [p]
                        df = mysql_db.all(sql, pamra)
                        if len(df)==0:
                            continue
                        df_list.append(df[0])
                    df_list = set(df_list)
                    list = []
                    for i in df_list:
                        dic = {}
                        dic['pro_no'] = i[0]
                        dic['username'] = i[1]
                        dic['project_name'] = i[2]
                        dic['address'] = i[3]
                        dic['capacity'] = float(i[4])
                        params1 = [i[5]]
                        sql14 = "SELECT cust_name FROM b_customer_manager WHERE user_id=%s"
                        sql15 = mysql_db.all(sql14, params1)
                        if len(sql15) == 0:
                            dic['manager_id'] = 0
                        else:
                            dic['manager_id'] = sql15[0][0]
                        dic['cust_contact'] = i[6]
                        dic['cust_phone'] = i[7]
                        dic['cust_company_name'] = i[8]
                        dic['manager_pro_url'] = i[9]
                        dic['cust_pro_url'] = i[10]
                        dic['org_name'] = i[11]
                        dic['org_qualification'] = i[12]
                        dic['img_checker'] = i[13]
                        dic['checker_phone'] = i[14]
                        dic['refuse_reason'] = i[15]
                        dic['create_time'] = int(time.mktime(i[17].timetuple()) * 1000)
                        list.append(dic)
                    return True, list, len(df_list)
                except Exception as msg:
                    return False, msg, 0


def find(parames: dict):
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
        parms3 = [df_userid[0][0]]
        sql4 = "SELECT id FROM b_customer_manager WHERE user_id=%s"
        sql5 = mysql_db.all(sql4, parms3)
        parms3 = [sql5[0][0]]
        sql6 = "SELECT pro_no,username,project_name,address,capacity,cust_contact,cust_phone,cust_company_name,org_name,org_qualification,img_checker,checker_phone,refuse_reason,create_time from b_job WHERE manager_id=%s ORDER BY b_job.create_time ASC"
        sql7 = mysql_db.all(sql6, parms3)
        columns = ['方案编号', '用户名', '项目名', '用户地址', '报装容量',
                   '联系人(客户)', '手机号码（客户）', '客户公司名称', '设计单位名称',
                   '单位资质', '审图联系人', '审图联系电话', '拒绝理由', '创建时间']
        return sql7,columns
    else:
        sql12 = "SELECT pro_no,username,project_name,address,capacity,manager_id,cust_contact,cust_phone,cust_company_name,org_name,org_qualification,img_checker,checker_phone,refuse_reason,create_time from b_job ORDER BY b_job.create_time ASC "
        sql13 = mysql_db.all(sql12)
        columns = ['方案编号', '用户名', '项目名', '用户地址', '报装容量', '负责的客户经理',
                   '联系人(客户)', '手机号码（客户）', '客户公司名称', '设计单位名称',
                   '单位资质', '审图联系人', '审图联系电话', '拒绝理由', '创建时间']
        return sql13,columns


curd_category = CRUDCategory()