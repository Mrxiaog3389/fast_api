# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 10:40
# @Author  : Xiaoyunlong
from fastapi import Header,Request
from datetime import datetime, timedelta
from typing import Any, Union,Optional
from jose import jwt
# from passlib.context import CryptContext
from app.setting import main_init
from fastapi.responses import JSONResponse
from fastapi import Depends, FastAPI, HTTPException
from starlette import status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import time

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")
config = main_init.Init_Config('81.69.29.78','cdbd','root','111')
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"

def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "username": str(subject)}
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    return encoded_jwt


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)
#
#
# def get_password_hash(password: str) -> str:
#     return pwd_context.hash(password)

def check_jwt_token(token: Optional[str] = Header(None)) -> Union[str, Any]:
    """
    解析验证 headers中为token的值 担任也可以用 Header(None, alias="Authentication") 或者 alias="X-token"
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(
            token,
            config.SECRET_KEY, algorithms=[ALGORITHM]
        )
        time1 = payload['exp']
        if time1 < time.time():
            return JSONResponse({'code': 401, 'data': None, 'message': "登录已过期"})
        else:
            return payload
    except (jwt.JWTError, jwt.ExpiredSignatureError, AttributeError):
        return JSONResponse({'code': 403, 'data': None, 'message': "用户未登录"})

