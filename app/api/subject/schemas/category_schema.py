from typing import Union, List
from pydantic import BaseModel, AnyHttpUrl, conint

class CategoryCreate(BaseModel):
    """
    新增题库分类
    """
    class_name: str
    admin_id: int
    appcode: str

class CategoryUpdate(BaseModel):
    """
    编辑题库分类
    """
    class_id: int
    class_name: str
    admin_id: int


class CategoryDel(BaseModel):
    """
    删除题库分类
    """
    class_id: int


class Questiontransfer(BaseModel):
    """
    转移题
    """
    question_id: str
    class_id: str
    admin_id: int

class QuestionDel(BaseModel):
    """
    删除题
    """
    question_id: int