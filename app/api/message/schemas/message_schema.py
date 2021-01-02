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
