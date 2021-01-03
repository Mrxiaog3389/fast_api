# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 10:40
# @Author  : Xiaoyunlong
from pydantic import BaseModel

class testCreate(BaseModel):
    """
    添加考试分类
    """
    class_name: str
    admin_id: int
    appcode: str

class testUpdate(BaseModel):
    """
    编辑考试分类
    """
    class_id: int
    class_name: str
    admin_id: int


class testDel(BaseModel):
    """
    删除题库分类
    """
    class_id: int


class testpaperDel(BaseModel):
    """
    删除试卷
    """
    exam_id: int
    uadmin_id:int

class Release(BaseModel):
    """
    发布考试
    """
    exam_id: int