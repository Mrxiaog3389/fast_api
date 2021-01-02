
from pydantic import BaseModel


class UserInfo(BaseModel):
    username: str
    password: str


class Userregister(BaseModel):
    username: str
    password: str
    password2:str
    nick_name: str
    face_img: str

class Useralter(BaseModel):
    id:str
    username: str
    password: str
    password2: str
    nick_name: str
    face_img: str
    roleIds:list

class Userdele(BaseModel):
    id: list


class Userpassword(BaseModel):
    userId: str
    newPwd: str
    oldPwd: str



class Useralterinformation(BaseModel):
    userId: str
    username: str
    nick_name: str
    face_img: str


class roledele(BaseModel):
    id: list


class roleincrease(BaseModel):
    description: str
    resourceList: list

class rolealter(BaseModel):
    id:str
    description: str
    resourceList: list

class resourcedele(BaseModel):
    id: list


class resourceincrease(BaseModel):
    groupName: str
    name: str
    method: str
    uri: str

class resourcealter(BaseModel):
    id: str
    name: str
    method: str
    uri: str