from app.setting import main_init
from database.db_con import Db_Connection
import time,json
from fastapi import Header
import pandas as pd
import datetime,uuid,hashlib

# config = main_init.Init_Config('192.168.4.131','app.gateway','root','123456!@#')
config = main_init.Init_Config('81.69.29.78','cdbd','root','111')
# config_crm = main_init.Init_Config('192.168.10.230','dxcrm','stocksir','stocksir1704!')
mysql_db=Db_Connection(config.msqusername,config.msqpassword,config.msqlserver,config.msqdb,config.msqcoding)
# crm_db=Db_Connection(config_crm.msqusername,config_crm.msqpassword,config_crm.msqlserver,config_crm.msqdb,config_crm.msqcoding)

class CRUDCategory(object):
    def login(self,parames: dict):
        try:
            params = [parames['username']]
            sql = 'SELECT id,username,`password` from sys_user WHERE username=%s'
            sql1 = 'SELECT username from sys_user'
            df = mysql_db.all(sql, params)
            sql_username_list = mysql_db.obtain_mysql_df(sql1)
            if len(df) == 0 or len(sql_username_list) == 0:
                return False
            else:
                return df, sql_username_list
            # params = [parames['username']]
            # sql = 'SELECT gs_admin.`password`,gs_admin.admin_id,gs_admin.img,gs_admin_token.key,gs_admin.username from gs_admin,gs_admin_token WHERE gs_admin.admin_id=gs_admin_token.admin_id and gs_admin.username=%s'
            # sql1 = 'SELECT username from gs_admin'
            # df=mysql_db.all(sql, params)
            # sql_username_list = mysql_db.obtain_mysql_df(sql1)
            # if len(df)== 0 or len(sql_username_list)==0:
            #     return False
            # else:
            #     return df,sql_username_list
        except Exception as errmsg:
            return False
    # def handle_limit_sql(self,parames: dict):
    #     """
    #     处理分页的规则
    #     """
    #     sql = f" limit {30 * (parames['curpage'] - 1)},30"
    #     return sql
    #
    # def get_log_list(self,parames: dict):
    #     """获取日志列表"""
    #     try:
    #         limit_sql= self.handle_limit_sql(parames)
    #         if parames['username'] != None and (parames['startingtime'] != None and parames['endtime'] != None):
    #             username = '%' + parames['username'] + '%'
    #             parame=[username,parames['startingtime'],parames['endtime']]
    #             all_sql = "SELECT module,action,useragent,ip,create_time from crm_admin_log202010 WHERE module LIKE %s and create_time BETWEEN  %s and %s ORDER BY create_time ASC " +limit_sql
    #             all_count_sql = f"select * from crm_admin_log202010 WHERE module LIKE %s and create_time BETWEEN  %s and %s"
    #             df = crm_db.all(all_sql, parame)
    #             list = []
    #             for i in df:
    #                 dic = {}
    #                 dic['module'] = i[0]
    #                 dic['action'] = i[1]
    #                 dic['useragent'] = i[2]
    #                 dic['ip'] = i[3]
    #                 dic['create_time'] = time.mktime(i[4].timetuple())
    #                 list.append(dic)
    #             df_count=crm_db.all(all_count_sql,parame)
    #             return list, len(df_count)
    #         elif parames['username'] != None:
    #             username = ['%' + parames['username'] + '%']
    #             all_sql = "SELECT module,action,useragent,ip,create_time from crm_admin_log202010 WHERE module LIKE %s ORDER BY create_time ASC " + limit_sql
    #             all_count_sql = f"select * from crm_admin_log202010 WHERE module LIKE %s"
    #             df = crm_db.all(all_sql, username)
    #             list = []
    #             for i in df:
    #                 dic = {}
    #                 dic['module'] = i[0]
    #                 dic['action'] = i[1]
    #                 dic['useragent'] = i[2]
    #                 dic['ip'] = i[3]
    #                 dic['create_time'] = time.mktime(i[4].timetuple())
    #                 list.append(dic)
    #             df_count = crm_db.all(all_count_sql, username)
    #             return list, len(df_count)
    #         elif parames['startingtime'] != None and parames['endtime'] != None:
    #             parame = [parames['startingtime'], parames['endtime']]
    #             all_sql = "SELECT module,action,useragent,ip,create_time from crm_admin_log202010 WHERE create_time BETWEEN  %s and %s ORDER BY create_time ASC " + limit_sql
    #             all_count_sql = f"select * from crm_admin_log202010 WHERE create_time BETWEEN  %s and %s"
    #             df = crm_db.all(all_sql, parame)
    #             list = []
    #             for i in df:
    #                 dic = {}
    #                 dic['module'] = i[0]
    #                 dic['action'] = i[1]
    #                 dic['useragent'] = i[2]
    #                 dic['ip'] = i[3]
    #                 dic['create_time'] = time.mktime(i[4].timetuple())
    #                 list.append(dic)
    #             df_count = crm_db.all(all_count_sql, parame)
    #             return list, len(df_count)
    #         else:
    #             all_sql = "SELECT module,action,useragent,ip,create_time from crm_admin_log202010 ORDER BY create_time ASC " + limit_sql
    #             all_count_sql = f"select * from crm_admin_log202010"
    #             df = crm_db.all(all_sql)
    #             list = []
    #             for i in df:
    #                 dic = {}
    #                 dic['module'] = i[0]
    #                 dic['action'] = i[1]
    #                 dic['useragent'] = i[2]
    #                 dic['ip'] = i[3]
    #                 dic['create_time'] = time.mktime(i[4].timetuple())
    #                 list.append(dic)
    #             df_count = crm_db.all(all_count_sql)
    #             return list, len(df_count)
    #     except Exception as msg:
    #         return False, msg, 0
    #
    # def get_admin_list(self,parames: dict):
    #     """获取管理员列表"""
    #     try:
    #         limit_sql= self.handle_limit_sql(parames)
    #         all_sql = "SELECT admin_id,building_id,datastatus,dtime,img,itime,lastlogintime,loginnum,mark,`password`,reason,seat_number,`status`,tel,truename,username,utime from gs_admin ORDER BY admin_id DESC " + limit_sql
    #         all_role_sql = "SELECT gs_admin_role.role_id,gs_role.role_name from gs_admin_role,gs_role WHERE gs_admin_role.role_id=gs_role.role_id and gs_admin_role.admin_id=%s"
    #         all_count_sql='SELECT * from gs_admin'
    #         df = mysql_db.all(all_sql)
    #         df_count = mysql_db.all(all_count_sql)
    #         if len(df) != 0:
    #             list = []
    #             for i in df:
    #                 dic = {}
    #                 dic['admin_id'] = i[0]
    #                 dic['building_id'] = i[1]
    #                 dic['datastatus'] = i[2]
    #                 dic['dtime'] = i[3]
    #                 dic['gangwei']=''
    #                 dic['img'] = i[4]
    #                 dic['itime'] = i[5]
    #                 dic['lastlogintime'] = i[6]
    #                 dic['loginnum'] = i[7]
    #                 dic['mark'] = i[8]
    #                 dic['password'] = i[9]
    #                 dic['privilegecode'] = ''
    #                 dic['reason'] = i[10]
    #                 roleidlist=[]
    #                 rolenames=[]
    #                 df_role = mysql_db.all(all_role_sql,i[0])
    #
    #                 if len(df_role) != 0 :
    #                     for j in df_role:
    #                         roleidlist.append(j[0])
    #                         rolenames.append(j[1])
    #                     dic['role_ids'] = roleidlist
    #                     dic['role_names'] = rolenames
    #                 else:
    #                     dic['role_ids'] = ''
    #                     dic['role_names'] = ''
    #                 dic['seat_number'] = i[11]
    #                 dic['status'] = i[12]
    #                 dic['tel'] = i[13]
    #                 dic['truename'] = i[14]
    #                 dic['username'] = str(i[15], encoding = "utf-8")
    #                 dic['utime'] = i[16]
    #                 list.append(dic)
    #             return list, len(df_count)
    #         else:
    #             list = []
    #             return list, len(df_count)
    #     except Exception as msg:
    #         return False, msg, 0
    #
    # def alter_password(self, parames: dict):
    #     try:
    #         sele_sql="SELECT `password` from gs_admin where username=%s"
    #         all_sql = "UPDATE gs_admin SET `password`=%s WHERE  username=%s  "
    #         sele_parms=[parames['username']]
    #         update_parms=[parames['new_password']]
    #         df = mysql_db.all(sele_sql,sele_parms)
    #         if parames['old_password'] != df[0][0]:
    #             old_password='原始密码不正确，请重新输入或联系管理员'
    #             return old_password
    #         else:
    #             mysql_db.commit_sql(update_parms, all_sql)
    #             return True
    #     except Exception as msg:
    #         return False, msg, 0
    #
    # def alter_data(self, parames: dict):
    #     try:
    #         all_sql = "UPDATE gs_admin SET img=%s WHERE  admin_id=%s  "
    #         update_parms=[parames['img'],parames['admin_id']]
    #         mysql_db.commit_sql(update_parms, all_sql)
    #         return True
    #     except Exception as msg:
    #         return False, msg, 0
    def handle_limit_sql(self,parames: dict):
        """
        处理分页的规则
        """
        sql = f" limit {parames['pagesize'] * (parames['curpage'] - 1)},{parames['pagesize']}"
        return sql

    def get_userid(self):
        try:
            all_sql = "SELECT * FROM sys_user"
            df = mysql_db.obtain_mysql_df(all_sql)
            return True, df
        except Exception as msg:
            return False, msg, 0

    def get_roleid(self):
        try:
            all_sql = "SELECT * FROM sys_role"
            df = mysql_db.obtain_mysql_df(all_sql)
            return True, df
        except Exception as msg:
            return False, msg, 0

    def userlist(self,parames: dict):
        try:
            limit_sql = self.handle_limit_sql(parames)
            sql = 'SELECT id,username,nick_name,face_img,create_time from sys_user ORDER BY create_time DESC ' + limit_sql
            sql_count = 'SELECT * from sys_user'
            sql_role = 'SELECT sys_role.id,sys_role.role_name from sys_role,sys_user_role WHERE sys_role.id=sys_user_role.role_id and sys_user_role.user_id=%s'
            df = mysql_db.all(sql)
            df_count = mysql_db.all(sql_count)
            list = []

            for i in df:
                roleIds = []
                roleNames = []
                dic = {}
                dic['id'] = i[0]
                dic['username'] = i[1]
                dic['nick_name'] = i[2]
                dic['face_img'] = i[3]
                dic['createTime'] = int(time.mktime(i[4].timetuple()) * 1000)
                df_role = mysql_db.all(sql_role, i[0])
                if len(df_role)==0:
                    roleIds.append(0)
                    roleNames.append(0)
                else:
                    for j in df_role:
                        roleIds.append(j[0])
                        roleNames.append(j[1])
                dic['roleIds'] = roleIds
                dic['roleNames'] = roleNames
                list.append(dic)
            return True, list, len(df_count)
        except Exception as errmsg:
            return False

    def useregister(self,parames: dict):
        try:
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            id = str(uuid.uuid1())
            bytes_url = hashlib.md5(parames['password'].encode())
            hashed = bytes_url.hexdigest()
            openid = ''
            role_id = ''
            params = [id, parames['username'], hashed, openid, parames['nick_name'], parames['face_img'], create_time, create_time]
            params1 = [id, role_id]
            sql = 'INSERT INTO sys_user(id,username,password,openid,nick_name,face_img,create_time,update_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
            sql1 = 'INSERT INTO sys_user_role(user_id,role_id) VALUES (%s,%s)'
            mysql_db.commit_sql(sql, params)
            mysql_db.commit_sql(sql1, params1)
            return True
        except Exception as errmsg:
            return False

    def useralter(self,parames: dict):
        try:
            bytes_url = hashlib.md5(parames['password'].encode())
            hashed = bytes_url.hexdigest()
            update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            params = [parames['username'], parames['nick_name'], hashed, parames['face_img'], update_time,
                      parames['id']]
            sql = 'UPDATE sys_user SET username =%s,nick_name=%s,`password`=%s,face_img=%s,update_time=%s WHERE id =%s'
            mysql_db.commit_sql(sql, params)
            params1 = [parames['id']]
            sql1 = 'DELETE FROM `sys_user_role` WHERE user_id = %s'
            mysql_db.commit_sql(sql1, params1)
            if len(parames['roleIds']) == 0:
                role_id = ''
                params2 = [parames['id'], role_id]
                sql2 = 'INSERT INTO sys_user_role(user_id,role_id) VALUES (%s,%s)'
                mysql_db.commit_sql(sql2, params2)
            else:
                for j in parames['roleIds']:
                    params2 = [parames['id'], j]
                    sql2 = 'INSERT INTO sys_user_role(user_id,role_id) VALUES (%s,%s)'
                    mysql_db.commit_sql(sql2, params2)
            return True
        except Exception as errmsg:
            return False

    def userdele(self,parames: dict):
        try:
            all_sql = "SELECT * from b_customer_manager ORDER BY create_time DESC "
            df = mysql_db.obtain_mysql_df(all_sql)
            customer_id=df['id'].tolist()

            for li in parames["id"]:
                if li in customer_id:
                    params = [li]
                    sql = 'DELETE FROM `sys_user` WHERE id = %s'
                    sql1 = 'DELETE FROM `sys_user_role` WHERE user_id = %s'
                    sql2 = 'DELETE FROM `b_customer_manager` WHERE user_id = %s'
                    mysql_db.commit_sql(sql, params)
                    mysql_db.commit_sql(sql1, params)
                    mysql_db.commit_sql(sql2, params)
                else:
                    params = [li]
                    sql = 'DELETE FROM `sys_user` WHERE id = %s'
                    sql1 = 'DELETE FROM `sys_user_role` WHERE user_id = %s'
                    mysql_db.commit_sql(sql, params)
                    mysql_db.commit_sql(sql1, params)
            return True
        except Exception as errmsg:
            return False

    def usercontrol(self):
        try:
            sql = "SELECT * from sys_role ORDER BY create_time DESC"
            df = mysql_db.obtain_mysql_df(sql)
            df['create_time'] = df['create_time'].apply(lambda x: int(time.mktime(x.timetuple()) * 1000))
            return True, df
        except Exception as msg:
            return False, msg, 0

    def alterpasswors(self,parames: dict):
        try:
            bytes_url = hashlib.md5(parames['newPwd'].encode())
            hashed = bytes_url.hexdigest()
            params = [hashed, parames['userId']]
            sql = 'UPDATE sys_user SET `password`=%s WHERE id =%s'
            mysql_db.commit_sql(sql, params)
            return True
        except Exception as msg:
            return False, msg, 0

    def user_information(self,parames: dict):
        try:
            params = [parames['userid']]
            sql = 'SELECT * FROM sys_user WHERE id=%s'
            df = mysql_db.all(sql, params)
            Dic = {}
            Dic['id'] = df[0][0]
            Dic['username'] = df[0][1]
            Dic['nick_name'] = df[0][4]
            Dic['face_img'] = df[0][5]
            Dic['create_time'] = int(time.mktime(df[0][6].timetuple()) * 1000)
            return True, Dic
        except Exception as msg:
            return False, msg, 0

    def user_alterinformation(self,parames: dict):
        try:
            params_rolename = [parames['userId']]
            sql_role = 'SELECT sys_role.role_name from sys_role,sys_user_role WHERE sys_role.id=sys_user_role.role_id and sys_user_role.user_id=%s'
            df_role = mysql_db.all(sql_role, params_rolename)
            rolename = []
            for i in df_role:
                rolename.append(i)
            update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if '客户经理' in rolename:
                params = [parames['username'], parames['nick_name'], parames['face_img'], update_time,
                          parames['userId']]
                params1 = [parames['face_img'], update_time, parames['userId']]
                sql4 = 'UPDATE sys_user SET username =%s,nick_name=%s,face_img=%s,update_time=%s WHERE id =%s'
                sql5 = 'UPDATE b_customer_manager SET image=%s,create_time=%s WHERE user_id =%s'
                mysql_db.commit_sql(sql4, params)
                mysql_db.commit_sql(sql5, params1)
                return True
            else:
                params = [parames['username'], parames['nick_name'], parames['face_img'], update_time,
                          parames['userId']]
                sql4 = 'UPDATE sys_user SET username =%s,nick_name=%s,face_img=%s,update_time=%s WHERE id =%s'
                mysql_db.commit_sql(sql4, params)
                return True
        except Exception as msg:
            return False, msg, 0

    def role_select(self):
        try:
            sql = "SELECT create_time,role_name,id FROM sys_role"
            df = mysql_db.obtain_mysql_df(sql)
            df['create_time']=df['create_time'].apply(lambda x :int(time.mktime(x.timetuple()) * 1000))
            return True, df
        except Exception as msg:
            return False, msg, 0

    def roledele(self,parames: dict):
        try:
            for li in parames["id"]:
                params = [li]
                sql = 'DELETE FROM `sys_role` WHERE id = %s'
                sql1 = 'DELETE FROM `sys_role_resource` WHERE role_id = %s'
                mysql_db.commit_sql(sql, params)
                mysql_db.commit_sql(sql1, params)
            return True
        except Exception as errmsg:
            return False

    def roleincrease(self,parames: dict):
        try:
            result, df = self.get_roleid()
            order = df['id'].tolist()
            list=[int(x) for x in order]
            if result:
                id = max(list) + 1
            else:
                id = 1
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            name = ''
            available = '1'

            if len(parames['description']) == 0:
                resource_id = ''
                params1 = [id, resource_id]
                sql1 = 'INSERT INTO sys_role_resource(role_id,resource_id) VALUES (%s,%s)'
                params = [id, name, parames['description'], available, create_time]
                sql = 'INSERT INTO sys_role(id,code,role_name,available,create_time) VALUES (%s,%s,%s,%s,%s)'
                mysql_db.commit_sql(sql, params)
                mysql_db.commit_sql(sql1, params1)
                return True
            else:
                params = [id, name, parames['description'], available, create_time]
                sql = 'INSERT INTO sys_role(id,code,role_name,available,create_time) VALUES (%s,%s,%s,%s,%s)'
                mysql_db.commit_sql(sql, params)
                for j in parames['resourceList']:
                    params2 = [id, j]
                    sql2 = 'INSERT INTO sys_role_resource(role_id,resource_id) VALUES (%s,%s)'
                    mysql_db.commit_sql(sql2, params2)
                return True

        except Exception as errmsg:
            return False

    def rolealter(self,parames: dict):
        try:
            uptade_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            name = ''
            sql = 'UPDATE sys_role SET code =%s,role_name=%s,create_time=%s WHERE id =%s'
            params = [name, parames['description'], uptade_time, parames['id']]
            mysql_db.commit_sql(sql, params)
            params1 = [parames['id']]
            sql1 = 'DELETE FROM `sys_role_resource` WHERE role_id = %s'
            mysql_db.commit_sql(sql1, params1)
            for j in parames['resourceList']:
                params2 = [parames['id'], j]
                sql2 = 'INSERT INTO sys_role_resource(role_id,resource_id) VALUES (%s,%s)'
                mysql_db.commit_sql(sql2, params2)
            return True

        except Exception as errmsg:
            return False

    def role_query(self,parames: dict):
        try:
            params = [parames['id']]
            sql = "SELECT sys_resource.id,sys_resource.`name` from sys_resource,sys_role_resource WHERE sys_resource.id=sys_role_resource.resource_id and sys_role_resource.role_id=%s"
            df = mysql_db.all(sql, params)
            data = []
            for s in df:
                dic = {}
                dic['id'] = s[0]
                dic['name'] = s[1]
                data.append(dic)
            return True, data
        except Exception as msg:
            return False, msg, 0

    def get_resource(self):
        try:
            all_sql = "SELECT * FROM sys_resource"
            df = mysql_db.obtain_mysql_df(all_sql)
            return True, df
        except Exception as msg:
            return False, msg, 0

    def resource_select(self):
        try:
            result, df = self.get_resource()
            li = df['group_name'].tolist()
            li = list(set(li))
            lis = []
            for i in li:
                Dic = {}
                Dic['groupName'] = i
                Dic['resourceList'] = []
                parms = [i]
                sql2 = "SELECT * FROM sys_resource WHERE group_name=%s"
                df = mysql_db.all(sql2, parms)
                for s in df:

                    dic = {}
                    dic['createTime'] = int(time.mktime(s[5].timetuple()) * 1000)
                    dic['groupName'] = s[6]
                    dic['id'] = s[0]
                    dic['method'] = s[1]
                    dic['role_name'] = s[3]
                    dic['name'] = s[4]
                    dic['uri'] = s[2]
                    Dic['resourceList'].append(dic)
                lis.append(Dic)
            return True, lis
        except Exception as msg:
            return False, msg, 0

    def resourcedele(self,parames: dict):
        try:
            for li in parames["id"]:
                params = [li]
                sql = 'DELETE FROM `sys_resource` WHERE id = %s'
                mysql_db.commit_sql(sql, params)
            return True
        except Exception as errmsg:
            return False

    def resourceincrease(self,parames: dict):
        try:
            result, df = self.get_resource()
            order = df['id'].tolist()
            list = [int(x) for x in order]
            if result:
                id = max(list) + 1
            else:
                id = 1
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            role_name = ''
            params = [id, parames['method'], parames['uri'], role_name, parames['name'], create_time,
                      parames['groupName']]
            sql = 'INSERT INTO sys_resource(id,method,uri,role_name,name,create_time,group_name) VALUES (%s,%s,%s,%s,%s,%s,%s)'
            mysql_db.commit_sql(sql, params)
            return True

        except Exception as errmsg:
            return False

    def resourcealter(self,parames: dict):
        try:
            uptade_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = 'UPDATE sys_resource SET name=%s,method=%s,uri=%s,create_time=%s WHERE id =%s'
            params = [parames['name'], parames['method'], parames['uri'], uptade_time, parames['id']]
            mysql_db.commit_sql(sql, params)
            return True

        except Exception as errmsg:
            return False

curd_category = CRUDCategory()