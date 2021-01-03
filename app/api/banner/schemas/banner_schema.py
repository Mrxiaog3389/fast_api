# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 10:40
# @Author  : Xiaoyunlong
from pydantic import BaseModel

class bannerCreate(BaseModel):
    """
    新增banner图片
    """
    banner_img: str
    banner_url: str

class bannerUpdate(BaseModel):
    """
    编辑banner图片
    """
    id: str
    banner_img: str
    banner_url: str


class bannerDel(BaseModel):
    """
    删除banner图片
    """
    id: str
