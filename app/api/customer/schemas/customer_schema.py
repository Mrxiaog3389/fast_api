from pydantic import BaseModel

class customerCreate(BaseModel):
    """
    新增客户经理接口
    """
    cust_name: str
    org_name: str
    tel: str
    phone: str
    company: str
    job_number: str
    profile: str
    image: str

class customerUpdate(BaseModel):
    """
    修改客户经理接口
    """
    id:str
    cust_name: str
    org_name: str
    tel: str
    phone: str
    company: str
    job_number: str
    profile: str
    image: str


class customerDel(BaseModel):
    """
    删除客户经理接口
    """
    lists: list
