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
