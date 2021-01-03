# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 10:40
# @Author  : Xiaoyunlong
from fastapi import APIRouter,Depends,Request,Query
from fastapi.responses import JSONResponse
import json,math,warnings
from app.common.logger import *
from .schemas import customer_schema
from .crud.customer import curd_category
from app.core.security import check_jwt_token
import numpy as np
from typing import Any, Union
router = APIRouter()

#过滤掉警告
warnings.filterwarnings('ignore')

@router.post("/insert", summary="新增客户经理")
async def customer_add(request:Request,cate_info: customer_schema.customerCreate,
                     token : Union[str, Any] = Depends(check_jwt_token)):
    if 'token' not in request.headers:
        return JSONResponse({'code': 403, 'data': None, 'message': "用户未登录"})
    increase_dict = {'cust_name': cate_info.cust_name,
                     'org_name': cate_info.org_name,
                     'tel': cate_info.tel,
                     'phone': cate_info.phone,
                     'company': cate_info.company,
                     'job_number': cate_info.job_number,
                     'profile': cate_info.profile,
                     'image': cate_info.image}
    result_add = curd_category.add_customer(increase_dict)
    if result_add:
        return {"code": 200, "message": "新增成功", "data": None}
    else:
        return {"code": 500, "message": "操作失败", "data": None}

@router.post("/alter", summary="修改客户经理")
async def customer_alter(request:Request,cate_info: customer_schema.customerUpdate,
                       token : Union[str, Any] = Depends(check_jwt_token)):
    if 'token' not in request.headers:
        return JSONResponse({'code': 403, 'data': None, 'message': "用户未登录"})
    increase_dict = {'id':cate_info.id,
                     'cust_name': cate_info.cust_name,
                     'org_name': cate_info.org_name,
                     'tel': cate_info.tel,
                     'phone': cate_info.phone,
                     'company': cate_info.company,
                     'job_number': cate_info.job_number,
                     'profile': cate_info.profile,
                     'image': cate_info.image}
    result_add = curd_category.update_customer(increase_dict)
    if result_add:
        return {"code": 200, "message": "编辑成功", "data": None}
    else:
        return {"code": 500, "message": "操作失败", "data": None}

@router.get("/sele", summary="查询客户经理")
async def customer_sele(request:Request,token : Union[str, Any] = Depends(check_jwt_token),
                      curpage: int = Query(1, ge=1, title="当前页"),
                      pagesize: int = Query(10, le=50, title="页码长度")):
    if 'token' not in request.headers:
        return JSONResponse({'code': 403, 'data': None, 'message': "用户未登录"})
    parames={'curpage':curpage,
             'pagesize':pagesize}
    result, df, df_count = curd_category.get_customer(parames)
    return_dict = {'code': 200, 'message': '操作成功', 'data': {'page_count': None, 'total_num': None, 'list': None}}
    if result and df_count == 0:
        return_dict['data']['page_count'] = 0
        return_dict['data']['total_num'] = 0
        return JSONResponse(return_dict)
    elif result and df_count / int(pagesize) < 1:
        return_dict['data']['page_count'] = 1
        return_dict['data']['total_num'] = df_count
        return_dict['data']['list'] = df
        return JSONResponse(return_dict)
    elif result:
        return_dict['data']['page_count'] = math.floor(df_count / int(pagesize)) + 1
        return_dict['data']['total_num'] = df_count
        return_dict['data']['list'] = df
        return JSONResponse(return_dict)
    else:
        return JSONResponse({"code": 500, "message": "操作失败", "data": None})

@router.delete("/dele", summary="删除客户经理")
async def customer_dele(request:Request,cate_info:customer_schema.customerDel,
                      token : Union[str, Any] = Depends(check_jwt_token)):
    if 'token' not in request.headers:
        return JSONResponse({'code': 403, 'data': None, 'message': "用户未登录"})
    #  获取传入的参数
    increase_dict = {'lists': cate_info.lists}
    result = curd_category.delete_customer(increase_dict)
    if result:
        return JSONResponse({"code": 200, "message": "操作成功", "data": None})
    else:
        return JSONResponse({"code": 500, "message": "操作失败", "data": None})



