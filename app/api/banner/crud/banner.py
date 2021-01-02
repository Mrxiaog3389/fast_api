from app.setting import main_init
from database.db_con import Db_Connection
import time,json,uuid
from fastapi import Header
import pandas as pd

config = main_init.Init_Config('81.69.29.78','cdbd','root','111')
mysql_db=Db_Connection(config.msqusername,config.msqpassword,config.msqlserver,config.msqdb,config.msqcoding)


class CRUDCategory(object):

    def add_banner(self,parames: dict, ) -> bool:
        try:
            id = str(uuid.uuid1())
            parames['id'] = id
            params = [parames['id'], parames['banner_img'], parames['banner_url']]
            sql = 'INSERT INTO b_banner(id,banner_img,banner_url) VALUES (%s,%s,%s)'
            mysql_db.commit_sql(sql, params)
            return True
        except Exception as errmsg:
            return False

    def get_banner(self):
        try:
            all_sql = "SELECT * FROM b_banner"
            df = mysql_db.obtain_mysql_df(all_sql)
            return True, df
        except Exception as msg:
            return False, msg, 0

    def update_banner(self,parames: dict):
        try:
            params = [parames['banner_img'], parames['banner_url'], parames['id']]
            sql = 'UPDATE b_banner SET banner_img =%s,banner_url=%s WHERE id =%s'
            mysql_db.commit_sql(sql, params)
            return True
        except Exception as msg:
            return False, msg, 0

    def delete_banner(self,parames: dict):
        try:
            params = [parames['id']]
            delete_sql = "DELETE FROM `b_banner` WHERE id = %s"
            mysql_db.commit_sql(delete_sql, params)
            return True
        except Exception as errmsg:
            return False


curd_category = CRUDCategory()