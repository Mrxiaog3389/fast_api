from app.setting import main_init
from database.db_con import Db_Connection
import time,json
import pandas as pd
config = main_init.Init_Config('192.168.4.131','app.exam','root','123456!@#')
mysql_db=Db_Connection(config.msqusername,config.msqpassword,config.msqlserver,config.msqdb,config.msqcoding)

class CRUDCategory(object):
    def add_subject(self,parames: dict) -> bool:
        """新增题库分类"""
        class_type = '2'
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

    def update_cate(self,ae_classify,parames: dict):
        """编辑题库分类"""
        utime = int(time.time())
        try:
            params = [parames['class_name'], utime,parames['uadmin_id'],parames['class_id']]
            sql = f'UPDATE {ae_classify} SET class_name=%s,utime=%s,uadmin_id=%s WHERE class_id =%s'
            mysql_db.commit_sql(sql,params)
            return True
        except Exception as msg:
            return False, msg, 0

    def get_all_count_num(self):
        """查询题库分类"""
        try:
            sql = "select class_id,count(1) AS counts from ae_questions WHERE datastatus=1 GROUP BY class_id"
            sql1="SELECT class_id,class_name from ae_classify WHERE class_type=2 and datastatus=1 and class_id  NOT IN (select class_id from ae_questions WHERE datastatus=1)"
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
            return True, res2,res
        except Exception as msg:
            return False, msg, 0

    def remove(self,ae_classify,class_id,parames: dict):
        """删除题库分类"""
        classid = parames[class_id]
        datastatus=0
        params = [datastatus, classid]
        delete_sql = f"UPDATE {ae_classify} SET datastatus =%s WHERE {class_id} = %s"
        status_result = mysql_db.commit_sql(delete_sql,params)
        # 获取 question_id
        params1=[classid]
        sql="select question_id from ae_questions WHERE datastatus=1 and class_id=%s"
        question_id_sele=mysql_db.all(sql,params1)
        # 将要删除的分类下的题转移至未分类下面
        question_id_upte="UPDATE ae_questions SET class_id =%s WHERE question_id = %s"
        for i in question_id_sele:
            params2=[datastatus,i[0]]
            mysql_db.commit_sql(question_id_upte, params2)
        return status_result

    def get_all(self,ae_classify):
        try:
            all_sql = f"SELECT class_id,class_name from {ae_classify} WHERE datastatus=1 and class_type=2"
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

    def get_question_list(self,parames: dict):
        """获取题目列表"""
        try:
            limit_sql= self.handle_limit_sql(parames)
            if parames['class_id'] != None and parames['question_title'] != None and parames['question_type'] != None:
                question_title = '%' + parames['question_title'] + '%'
                parame=[parames['class_id'],parames['question_type'],question_title]
                all_sql = f"SELECT class_id,question_id,question_title,question_type,correct_option,uadmin_id,itime, utime,options from ae_questions where datastatus=1 and class_id=%s and question_type=%s and question_title LIKE %s ORDER BY question_id ASC " +limit_sql
                all_count_sql = f"select * from ae_questions WHERE datastatus=1 and class_id=%s and question_type=%s and question_title LIKE %s"
                df = mysql_db.all(all_sql, question_title)
                list = []
                for i in df:
                    dic = {}
                    dic['class_id'] = i[0]
                    dic['question_id'] = i[1]
                    dic['question_title'] = i[2]
                    dic['question_type'] = i[3]
                    dic['correct_option'] = i[4]
                    dic['uadmin_id'] = i[5]
                    dic['itime'] = i[6]
                    dic['utime'] = i[7]
                    dic['options'] = json.loads(i[8])
                    list.append(dic)
                df_count=mysql_db.all(all_count_sql,parame)
                return list, len(df_count)
            elif parames['class_id'] != None and parames['question_type'] != None:
                all_sql = f"SELECT class_id,question_id,question_title,question_type,correct_option,uadmin_id,itime, utime,options from ae_questions where datastatus=1 and class_id={parames['class_id']} and question_type={parames['question_type']} ORDER BY question_id ASC " +limit_sql
                all_count_sql = f"select COUNT(*) from ae_questions WHERE datastatus=1 and class_id={parames['class_id']} and question_type={parames['question_type']}"
                df = mysql_db.obtain_mysql_df(all_sql)
                df['options']=df['options'].apply(lambda x: json.loads(x))
                df_count=mysql_db.obtain_mysql_count(all_count_sql)
                return df, df_count
            elif parames['class_id'] != None and parames['question_title'] != None:
                question_title = '%' + parames['question_title'] + '%'
                parame=[parames['class_id'],question_title]
                all_sql = f"SELECT class_id,question_id,question_title,question_type,correct_option,uadmin_id,itime, utime,options from ae_questions where datastatus=1 and class_id=%s and question_title LIKE %s ORDER BY question_id ASC " +limit_sql
                all_count_sql = f"select * from ae_questions WHERE datastatus=1 and class_id=%s and question_title LIKE %s"
                df = mysql_db.all(all_sql, question_title)
                list = []
                for i in df:
                    dic = {}
                    dic['class_id'] = i[0]
                    dic['question_id'] = i[1]
                    dic['question_title'] = i[2]
                    dic['question_type'] = i[3]
                    dic['correct_option'] = i[4]
                    dic['uadmin_id'] = i[5]
                    dic['itime'] = i[6]
                    dic['utime'] = i[7]
                    dic['options'] = json.loads(i[8])
                    list.append(dic)
                df_count=mysql_db.all(all_count_sql,parame)
                return list, len(df_count)
            elif parames['question_type'] != None and parames['question_title'] != None:
                question_title = '%' + parames['question_title'] + '%'
                parame=[parames['question_type'],question_title]
                all_sql = f"SELECT class_id,question_id,question_title,question_type,correct_option,uadmin_id,itime, utime,options from ae_questions where datastatus=1 and question_type=%s and question_title LIKE %s ORDER BY question_id ASC " +limit_sql
                all_count_sql = f"select * from ae_questions WHERE datastatus=1 and question_type=%s and question_title LIKE %s"
                df = mysql_db.all(all_sql, question_title)
                list = []
                for i in df:
                    dic = {}
                    dic['class_id'] = i[0]
                    dic['question_id'] = i[1]
                    dic['question_title'] = i[2]
                    dic['question_type'] = i[3]
                    dic['correct_option'] = i[4]
                    dic['uadmin_id'] = i[5]
                    dic['itime'] = i[6]
                    dic['utime'] = i[7]
                    dic['options'] = json.loads(i[8])
                    list.append(dic)
                df_count=mysql_db.all(all_count_sql,parame)
                return list, len(df_count)
            elif parames['class_id'] != None:
                all_sql = f"SELECT class_id,question_id,question_title,question_type,correct_option,uadmin_id,itime, utime,options from ae_questions where datastatus=1 and class_id={parames['class_id']} ORDER BY question_id ASC " +limit_sql
                all_count_sql = f"select COUNT(*) from ae_questions WHERE datastatus=1 and class_id={parames['class_id']}"
                df = mysql_db.obtain_mysql_df(all_sql)
                df['options']=df['options'].apply(lambda x: json.loads(x))
                df_count=mysql_db.obtain_mysql_count(all_count_sql)
                return df, df_count
            elif parames['question_title'] != None:
                question_title = '%' + parames['question_title'] + '%'
                all_sql = "SELECT class_id,question_id,question_title,question_type,correct_option,uadmin_id,itime, utime,options from ae_questions WHERE datastatus=1 and question_title LIKE %s ORDER BY question_id ASC "+limit_sql
                df = mysql_db.all(all_sql,question_title)
                list=[]
                for i in df:
                    dic={}
                    dic['class_id']=i[0]
                    dic['question_id'] = i[1]
                    dic['question_title'] = i[2]
                    dic['question_type'] = i[3]
                    dic['correct_option'] = i[4]
                    dic['uadmin_id'] = i[5]
                    dic['itime'] = i[6]
                    dic['utime'] = i[7]
                    dic['options'] = json.loads(i[8])
                    list.append(dic)
                all_count_sql = "select * from ae_questions WHERE datastatus=1 and question_title LIKE %s"
                df_count=mysql_db.all(all_count_sql,question_title)
                return list, len(df_count)
            elif parames['question_type'] != None:
                all_sql = f"SELECT class_id,question_id,question_title,question_type,correct_option,uadmin_id,itime, utime,options from ae_questions WHERE datastatus=1 and question_type = {parames['question_type']} ORDER BY question_id ASC " +limit_sql
                all_count_sql = f"select COUNT(*) from ae_questions WHERE datastatus=1 and question_type={parames['question_type']}"
                df = mysql_db.obtain_mysql_df(all_sql)
                df['options']=df['options'].apply(lambda x: json.loads(x))
                df_count=mysql_db.obtain_mysql_count(all_count_sql)
                return df, df_count
            else:
                all_sql = f"SELECT class_id,question_id,question_title,question_type,correct_option,uadmin_id,itime, utime,options from ae_questions WHERE datastatus=1 "+"ORDER BY question_id ASC " +limit_sql
                all_count_sql = "select COUNT(*) from ae_questions WHERE datastatus=1"
                df = mysql_db.obtain_mysql_df(all_sql)
                df['options']=df['options'].apply(lambda x: json.loads(x))
                df_count=mysql_db.obtain_mysql_count(all_count_sql)
                return df, df_count
        except Exception as msg:
            return False, msg, 0

    def get_details_list(self,parames: dict):
        """获取题目列表"""
        try:
            params=[parames['question_id']]
            all_sql = f"SELECT analysis,class_id,correct_option,options,question_id,question_title,question_type from ae_questions WHERE datastatus=1 and question_id=%s"
            df = mysql_db.all(all_sql,params)
            return df
        except Exception as msg:
            return False, msg, 0

    def update_question(self,ae_classify,parames: dict):
        """转移题"""
        utime = int(time.time())
        try:
            params = [parames['class_id'], utime,parames['uadmin_id'],parames['question_id']]
            sql = f'UPDATE {ae_classify} SET class_id=%s,utime=%s,uadmin_id=%s WHERE question_id =%s'
            mysql_db.commit_sql(sql,params)
            return True
        except Exception as msg:
            return False, msg, 0

    def remove_question(self,parames: dict):
        """删除题"""
        datastatus = 0
        try:
            params = [datastatus,parames['question_id']]
            sql = f'UPDATE ae_questions SET datastatus =%s WHERE question_id =%s'
            mysql_db.commit_sql(sql,params)
            return True
        except Exception as msg:
            return False, msg, 0

curd_category = CRUDCategory()