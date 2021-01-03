# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 10:40
# @Author  : Xiaoyunlong
from fastapi import APIRouter
from . import subject,test,user,banner,customer,message,material,project,home
api_router = APIRouter()
api_router.include_router(home.router, prefix="/home", tags=["首页"])
api_router.include_router(user.router, prefix="/user", tags=["用户管理"])
api_router.include_router(banner.router, prefix="/banner", tags=["banner图片管理"])
api_router.include_router(customer.router, prefix="/accountcustomer", tags=["客户经理管理"])
api_router.include_router(message.router, prefix="/message", tags=["消息通知管理"])
api_router.include_router(material.router, prefix="/data", tags=["资料管理"])
api_router.include_router(project.router, prefix="/project", tags=["项目管理"])
api_router.include_router(subject.router, prefix="/subject", tags=["题库管理"])
api_router.include_router(test.router, prefix="/test", tags=["考试管理"])