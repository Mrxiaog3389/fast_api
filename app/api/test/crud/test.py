# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 10:40
# @Author  : Xiaoyunlong
from app.setting import main_init
from database.db_con import Db_Connection
import time,json
from fastapi import Header
import pandas as pd
config = main_init.Init_Config('192.168.4.131','app.exam','root','123456!@#')
config_user = main_init.Init_Config('192.168.4.131','app.user','root','123456!@#')
mysql_db=Db_Connection(config.msqusername,config.msqpassword,config.msqlserver,config.msqdb,config.msqcoding)
mysql_db_user=Db_Connection(config_user.msqusername,config_user.msqpassword,config_user.msqlserver,config_user.msqdb,config_user.msqcoding)


class CRUDCategory(object):

    def add_test(self,parames: dict) -> bool:
        class_type = '1'
        itime = int(time.time())
        utime = 0
        dtime = 0
        uadmin_id = 0
        datastatus = 1
        client=parames['user-agent'].headers['user-agent']
        try:
            params = [class_type,parames['class_name'], itime,utime,dtime,parames['admin_id'],uadmin_id,datastatus,parames['appcode'],client]
            sql = 'INSERT INTO ae_classify(class_type,class_name,itime,utime,dtime,iadmin_id,uadmin_id,datastatus,appcode,client) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mysql_db.commit_sql(sql, params)
            return True
        except Exception as errmsg:
            return False

    def get_all_count_num(self):
        try:
            sql = "select class_id,count(1) AS counts from ae_exam WHERE datastatus=1 GROUP BY class_id"
            sql1="SELECT class_id,class_name from ae_classify WHERE class_type=1 and datastatus=1 and class_id  NOT IN (select class_id from ae_exam WHERE datastatus=1)"
            df = mysql_db.all(sql)
            df1 = mysql_db.obtain_mysql_df(sql1)
            list=[]
            for i in range(len(df1['class_id'].tolist())):
                list.append(0)
            df1['count_num']=list
            class_id=[]
            count_num=[]
            for j in df:
                class_id.append(j[0])
                count_num.append(j[1])
            res=pd.DataFrame({'class_id':class_id,'count_num':count_num})
            ae_classify = 'ae_classify'
            results, results_df = self.get_all(ae_classify)
            res1=pd.merge(res,results_df,how='inner',on=['class_id'])
            res1=res1[['class_id','class_name','count_num']]
            res2 = pd.concat([res1, df1])
            # res2=res2.sort_values(by='class-id')
            return True, res2,res
        except Exception as msg:
            return False, msg, 0

    def get_all(self,ae_classify):
        try:
            all_sql = f"SELECT class_id,class_name from {ae_classify} WHERE datastatus=1 and class_type=1"
            df = mysql_db.obtain_mysql_df(all_sql)
            return True, df
        except Exception as msg:
            return False, msg, 0

    def update_test(self,ae_classify,parames: dict):
        utime = int(time.time())
        try:
            params = [parames['class_name'], utime,parames['uadmin_id'],parames['class_id']]
            sql = f'UPDATE {ae_classify} SET class_name=%s,utime=%s,uadmin_id=%s WHERE class_id =%s'
            mysql_db.commit_sql(sql,params)
            return True
        except Exception as msg:
            return False, msg, 0

    def remove(self,parames: dict):
        datastatus = 0
        params = [datastatus, parames['class_id']]
        delete_sql = "UPDATE ae_classify SET datastatus =%s WHERE class_id = %s"
        status_result = mysql_db.commit_sql(delete_sql, params)
        # 获取 exam_id
        params1 = [parames['class_id']]
        sql = "select exam_id from ae_exam WHERE datastatus=1 and class_id=%s"
        question_id_sele = mysql_db.all(sql, params1)
        # 将要删除的分类下的考试转移至未分类下面
        question_id_upte = "UPDATE ae_exam SET class_id =%s WHERE exam_id = %s"
        for i in question_id_sele:
            params2 = [datastatus, i[0]]
            mysql_db.commit_sql(question_id_upte, params2)
        return status_result

    def update_Release(self,ae_classify,parames: dict):
        utime = int(time.time())
        publish_status=1
        try:
            params = [publish_status, utime,parames['exam_id']]
            sql = f'UPDATE {ae_classify} SET publish_status=%s,utime=%s WHERE exam_id =%s'
            mysql_db.commit_sql(sql,params)
            return True
        except Exception as msg:
            return False, msg, 0

    def get_review(self,parames: dict):
        try:
            params=[parames['member_exam_id']]
            sql="SELECT member_exam_id,exam_id,member_id,grade,true_num,false_num,not_num,exam_time,itime from ae_member_exam where datastatus=1 and member_exam_id=%s"
            df = mysql_db.all(sql,params)
            if len(df)==0:
                return False
            else:
                sql1="SELECT answer_option from ae_member_exam_record where member_exam_id=%s"
                sql2="SELECT exam_question_id,serial_num,question_type,question_title,correct_option,analysis,options from ae_exam_question where datastatus=1 and exam_id=%s"
                params1 = [df[0][1]]
                df1 = mysql_db.all(sql1, params)
                df2 = mysql_db.all(sql2, params1)
                return df,df1,df2

        except Exception as msg:
            return False

    def handle_limit_sql(self,parames: dict):
        """
        处理分页的规则
        """
        sql = f" limit {parames['pagesize'] * (parames['curpage'] - 1)},{parames['pagesize']}"
        return sql

    def get_test_list(self,parames: dict):
        try:
            if parames['class_id'] != None and parames['name'] != None:
                limit_sql= self.handle_limit_sql(parames)
                paras=[parames['class_id'],'%'+parames['name']+'%']
                all_sql = "SELECT exam_id,img,name,itime,publish_status from ae_exam WHERE datastatus=1 and class_id=%s and name LIKE %s"+"ORDER BY exam_id ASC " +limit_sql
                all_count_sql = "select * from ae_exam WHERE datastatus=1 and class_id=%s and name LIKE %s"
                df = mysql_db.all(all_sql,paras)
                df_count=mysql_db.all(all_count_sql,paras)
                list=[]
                for i in df:
                    dic={}
                    dic['exam_id']=i[0]
                    dic['img'] = i[1]
                    dic['name'] = i[2]
                    dic['itime'] = i[3]
                    dic['publish_status'] = i[4]
                    list.append(dic)
                return list,len(df_count)
            elif parames['class_id'] != None:
                limit_sql = self.handle_limit_sql(parames)
                paras = [parames['class_id']]
                all_sql = "SELECT exam_id,img,name,itime,publish_status from ae_exam WHERE datastatus=1 and class_id=%s ORDER BY exam_id ASC " + limit_sql
                all_count_sql = "select * from ae_exam WHERE datastatus=1 and class_id=%s"
                df = mysql_db.all(all_sql,paras)
                df_count = mysql_db.all(all_count_sql,paras)
                list = []
                for i in df:
                    dic = {}
                    dic['exam_id'] = i[0]
                    dic['img'] = i[1]
                    dic['name'] = i[2]
                    dic['itime'] = i[3]
                    dic['publish_status'] = i[4]
                    list.append(dic)
                return list,len(df_count)
            elif parames['name'] != None:
                limit_sql = self.handle_limit_sql(parames)
                paras = ['%' + parames['name'] + '%']
                all_sql = f"SELECT exam_id,img,name,itime,publish_status from ae_exam WHERE datastatus=1 and name LIKE %s" + "ORDER BY exam_id ASC " + limit_sql
                all_count_sql = f"select COUNT(*) from ae_exam WHERE datastatus=1 and name LIKE %s"
                df = mysql_db.all(all_sql,paras)
                df_count = mysql_db.all(all_count_sql,paras)
                list = []
                for i in df:
                    dic = {}
                    dic['exam_id'] = i[0]
                    dic['img'] = i[1]
                    dic['name'] = i[2]
                    dic['itime'] = i[3]
                    dic['publish_status'] = i[4]
                    list.append(dic)
                return list, len(df_count)
            else:
                limit_sql = self.handle_limit_sql(parames)
                all_sql = f"SELECT exam_id,img,name,itime,publish_status from ae_exam WHERE datastatus=1 " + "ORDER BY exam_id ASC " + limit_sql
                all_count_sql = f"select COUNT(*) from ae_exam WHERE datastatus=1"
                df = mysql_db.obtain_mysql_df(all_sql)
                df_count = mysql_db.obtain_mysql_count(all_count_sql)
                return df, df_count
        except Exception as msg:
            return False, msg, 0

    def get_details_test_list(self,parames: dict):
        try:
            params=[parames['exam_id']]
            sql = "SELECT class_id,name,img,intro,answer_show,publish_status from ae_exam WHERE datastatus=1 and exam_id=%s"
            sql1= "SELECT exam_question_id,serial_num,question_type,question_title,options,correct_option,analysis,score from ae_exam_question WHERE datastatus=1 and exam_id=%s"
            df = mysql_db.all(sql,params)
            df1 = mysql_db.all(sql1, params)
            return df,df1
        except Exception as msg:
            return False, msg, 0

    def get_review_list(self,parames: dict):
        try:
            if parames['member_name'] != None:
                limit_sql= self.handle_limit_sql(parames)
                all_sql = f"SELECT exam_id,grade,itime,member_exam_id,member_id from ae_member_exam WHERE exam_id={parames['exam_id']} GROUP BY member_exam_id DESC "+limit_sql
                all_count_sql = f"select COUNT(*) from ae_member_exam WHERE datastatus=1 and exam_id={parames['exam_id']}"
                df = mysql_db.all(all_sql)
                df_count=mysql_db.obtain_mysql_count(all_count_sql)
                return df,df_count
            else:
                limit_sql = self.handle_limit_sql(parames)
                all_sql = f"SELECT exam_id,grade,itime,member_exam_id,member_id from ae_member_exam WHERE exam_id={parames['exam_id']} GROUP BY member_exam_id DESC " + limit_sql
                all_count_sql = f"select COUNT(*) from ae_member_exam WHERE datastatus=1 and exam_id={parames['exam_id']}"
                df = mysql_db.all(all_sql)
                df_count = mysql_db.obtain_mysql_count(all_count_sql)
                return df, df_count
        except Exception as msg:
            return False, msg, 0

    def get_user_list(self):
        """用户信息查询"""
        try:
            all_sql = f"SELECT wx_headimgurl,member_id,member_name from member"
            df = mysql_db_user.obtain_mysql_df(all_sql)
            return df
        except Exception as msg:
            return False, msg, 0

    def remove_test(self, parames: dict):
        """删除试卷"""
        utime = int(time.time())
        datastatus = 0
        try:
            params = [datastatus, utime, parames['uadmin_id'], parames['exam_id']]
            sql = f'UPDATE ae_exam SET datastatus =%s,utime=%s,uadmin_id=%s WHERE exam_id =%s'
            mysql_db.commit_sql(sql, params)
            return True
        except Exception as msg:
            return False, msg, 0


curd_category = CRUDCategory()