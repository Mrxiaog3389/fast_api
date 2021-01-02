# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 10:40
# @Author  : Xiaoyunlong
from functools import wraps
from fastapi import Request,Header
from fastapi.responses import JSONResponse
from app.setting import main_init
from database.db_con import Db_Connection
# from redis import Redis
from jose import jwt
from typing import Any, Union,Optional

# config = main_init.Init_Config('192.168.4.131','app.exam','root','123456!@#')
config = main_init.Init_Config('81.69.29.78','cdbd','root','111')
mysql_db=Db_Connection(config.msqusername,config.msqpassword,config.msqlserver,config.msqdb,config.msqcoding)
# xtredis = Redis(host=config.rediserver, port=config.rediport)

async def Jurisdiction(token: Optional[str] = Header(None)):
    ALGORITHM = "HS256"
    payload = jwt.decode(
        token,
        config.SECRET_KEY, algorithms=[ALGORITHM]
    )
    username = payload['username']

    params1 = [username]
    sql1 = "select id from sys_user WHERE username=%s"
    df_userid = mysql_db.all(sql1, params1)
    params_rolename = [df_userid[0][0]]
    sql_role = 'SELECT sys_role.id,sys_role.role_name from sys_role,sys_user_role WHERE sys_role.id=sys_user_role.role_id and sys_user_role.user_id=%s'
    df_role = mysql_db.all(sql_role, params_rolename)
    rolename = []
    role_id=[]
    for i in df_role:
        role_id.append(i[0])
        rolename.append(i[1])

    uri=[]
    for u in role_id:
        params1 = [u]
        sql2 = "select sys_resource.uri from sys_resource,sys_role_resource where sys_resource.id=sys_role_resource.resource_id and sys_role_resource.role_id=%s"
        sql3 = mysql_db.all(sql2, params1)
        for i in sql3:
            uri.append(i[0])
    return uri