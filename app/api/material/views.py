# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 10:40
# @Author  : Xiaoyunlong
from fastapi import APIRouter,Depends,Request,Query
from fastapi.responses import JSONResponse
import json,math,warnings
from app.common.logger import *
from .schemas import material_schema
from .crud.material import curd_category
from app.core.security import check_jwt_token
import numpy as np
from typing import Any, Union
router = APIRouter()

#过滤掉警告
warnings.filterwarnings('ignore')

@router.get("/sele", summary="查询资料")
async def data_sele(request:Request,token : Union[str, Any] = Depends(check_jwt_token),
                      curpage: int = Query(1, ge=1, title="当前页"),
                      pagesize: int = Query(10, le=50, title="页码长度")):
    if 'token' not in request.headers:
        return JSONResponse({'code': 403, 'data': None, 'message': "用户未登录"})
    parames={'curpage':curpage,
             'pagesize':pagesize,
             'token':request.headers['token']}
    result, df, df_count = curd_category.get_material(parames)
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

@router.post("/insert", summary="新增资料")
async def data_add(request:Request,cate_info: material_schema.dataCreate,
                     token : Union[str, Any] = Depends(check_jwt_token)):
    if 'token' not in request.headers:
        return JSONResponse({'code': 403, 'data': None, 'message': "用户未登录"})
    increase_dict = {'name': cate_info.name,
                     'url': cate_info.url,
                     'token': request.headers['token']}
    result_add = curd_category.add_material(increase_dict)
    if result_add:
        return {"code": 200, "message": "新增成功", "data": None}
    else:
        return {"code": 500, "message": "操作失败", "data": None}

@router.post("/alter", summary="修改资料")
async def data_alter(request:Request,cate_info: material_schema.dataUpdate,
                       token : Union[str, Any] = Depends(check_jwt_token)):
    if 'token' not in request.headers:
        return JSONResponse({'code': 403, 'data': None, 'message': "用户未登录"})
    increase_dict = {'id':cate_info.id,
                     'name':cate_info.name,
                     'url': cate_info.url}
    result_add = curd_category.update_material(increase_dict)
    if result_add:
        return {"code": 200, "message": "编辑成功", "data": None}
    else:
        return {"code": 500, "message": "操作失败", "data": None}

@router.delete("/dele", summary="删除资料")
async def data_dele(request:Request,cate_info:material_schema.dataDel,
                      token : Union[str, Any] = Depends(check_jwt_token)):
    if 'token' not in request.headers:
        return JSONResponse({'code': 403, 'data': None, 'message': "用户未登录"})
    #  获取传入的参数
    increase_dict = {'id': cate_info.id}
    result, df = curd_category.get_id()
    uuid = df['id'].tolist()
    for i in increase_dict['id']:
        if i in uuid and result:
            result1 = curd_category.delete_material(i)
            if result1:
                return JSONResponse({"code": 200, "message": "操作成功", "data": None})
            else:
                return JSONResponse({"code": 500, "message": "操作失败", "data": None})
        else:
            return JSONResponse({"code": 409, "message": "删除的资料模板不存在", "data": None})
