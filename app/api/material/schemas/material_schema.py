# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 10:40
# @Author  : Xiaoyunlong
from pydantic import BaseModel

class dataCreate(BaseModel):
    """
    新增资料
    """
    name: str
    url: str

class dataUpdate(BaseModel):
    """
    修改资料
    """
    id:str
    name: str
    url: str


class dataDel(BaseModel):
    """
    删除资料
    """
    id: list
