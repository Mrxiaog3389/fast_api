from fastapi import APIRouter,Depends,Request,Query
from fastapi.responses import JSONResponse
import json,math,warnings
from app.common.logger import *
from .schemas import home_schema
from .crud.home import curd_category
from app.core.security import check_jwt_token
import numpy as np
from typing import Any, Union
router = APIRouter()

#过滤掉警告
warnings.filterwarnings('ignore')

@router.post("/analysis", summary="业务分析")
async def home_analysis(token : Union[str, Any] = Depends(check_jwt_token)):
    increase_dict = {'token':token}
    list = curd_category.analysis(increase_dict)
    return_dict = {'code': '200', 'message': '操作成功', 'data': {'list': None}}
    return_dict['data']['list'] = list
    return JSONResponse(return_dict)

@router.post("/year", summary="数据统计")
async def home_year(year:int,month:int,
                    token : Union[str, Any] = Depends(check_jwt_token)):
    increase_dict = {'token':token,
                     'year':year,
                     'month':month}
    list = curd_category.year(increase_dict)
    return_dict = {'code': '200', 'message': '操作成功', 'data': {'list': None}}
    return_dict['data']['list'] = list
    return JSONResponse(return_dict)