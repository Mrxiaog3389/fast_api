# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 10:40
# @Author  : Xiaoyunlong
from pydantic import BaseModel

class messageCreate(BaseModel):
    """
    新增消息接口
    """
    title: str
    remark: str
    content: str
    url: str
    object: int

class messageUpdate(BaseModel):
    """
    修改消息接口
    """
    id:str
    title: str
    remark: str
    content: str
    url: str
    object: int


class messageDel(BaseModel):
    """
    删除消息通知接口
    """
    lists: list
