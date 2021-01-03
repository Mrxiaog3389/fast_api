# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 10:40
# @Author  : Xiaoyunlong
from fastapi import APIRouter,Depends,Request
from fastapi.responses import JSONResponse
import json,math,warnings
from app.common.logger import *
from .schemas import banner_schema
from .crud.banner import curd_category
from app.common.role_auth import Jurisdiction
from app.core.security import check_jwt_token
import numpy as np
from typing import Any, Union
router = APIRouter()

#过滤掉警告
warnings.filterwarnings('ignore')

@router.post("/insert", summary="banner图片新增")
async def banner_add(request:Request,cate_info: banner_schema.bannerCreate,
                     token : Union[str, Any] = Depends(check_jwt_token)):
    if 'token' not in request.headers:
        return JSONResponse({'code': 403, 'data': None, 'message': "用户未登录"})
    increase_dict = {'banner_img': cate_info.banner_img,
                     'banner_url': cate_info.banner_url}
    result_add = curd_category.add_banner(increase_dict)
    if result_add:
        return {"code": 200, "message": "新增成功", "data": None}
    else:
        return {"code": 500, "message": "操作失败", "data": None}

@router.post("/alter", summary="banner图片修改")
async def banner_alter(request:Request,cate_info: banner_schema.bannerUpdate,
                       token : Union[str, Any] = Depends(check_jwt_token)):
    if 'token' not in request.headers:
        return JSONResponse({'code': 403, 'data': None, 'message': "用户未登录"})
    increase_dict = {'id': cate_info.id,
                     'banner_img':cate_info.banner_img,
                     'banner_url': cate_info.banner_url}
    result_add = curd_category.update_banner(increase_dict)
    if result_add:
        return {"code": 200, "message": "编辑成功", "data": None}
    else:
        return {"code": 500, "message": "操作失败", "data": None}

@router.get("/select", summary="banner图片查询")
async def banner_sele(request:Request,token : Union[str, Any] = Depends(check_jwt_token),
                      Jur_path=Depends(Jurisdiction)):
    if 'token' not in request.headers:
        return JSONResponse({'code': 403, 'data': None, 'message': "用户未登录"})
    path = request.url.path
    if path not in Jur_path:
        return JSONResponse({'code': 401, 'data': None, 'message': "您无权限访问"})
    return_dict = {'code': 200, 'message': '操作成功', 'data': {'list': None}}
    result, df = curd_category.get_banner()
    if result:
        if len(df) != 0:
            return_dict['data']['list'] = df.to_dict(orient='records')
            return JSONResponse(return_dict)
        else:
            return JSONResponse(return_dict)
    else:
        return JSONResponse({"code": 500, "message": "操作失败", "data": None})

@router.delete("/dele", summary="banner图片删除")
async def banner_dele(request:Request,cate_info:banner_schema.bannerDel,
                      token : Union[str, Any] = Depends(check_jwt_token)):
    if 'token' not in request.headers:
        return JSONResponse({'code': 403, 'data': None, 'message': "用户未登录"})
    #  获取传入的参数
    results, results_df = curd_category.get_banner()
    uuid = results_df['id'].tolist()
    class_id_dict={}
    if cate_info.id in uuid:
        class_id_dict['id']=cate_info.id
        results = curd_category.delete_banner(class_id_dict)
        if results:
            return JSONResponse({"code": 200, "message": "删除成功", "data": None})
        else:
            return JSONResponse(json.dumps({"code": 500, "message": "操作失败", "data": None}))
    else:
        return JSONResponse(json.dumps({"code": 409, "message": "删除的题库不存在", "data": None}))



