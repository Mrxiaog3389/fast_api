from fastapi import APIRouter,Depends,Request,Query
from fastapi.responses import JSONResponse
import json,math,warnings
from app.common.logger import *
from .schemas import message_schema
from .crud.message import curd_category
from app.core.security import check_jwt_token
import numpy as np
from typing import Any, Union
router = APIRouter()

#过滤掉警告
warnings.filterwarnings('ignore')

@router.post("/insert", summary="新增消息通知")
async def message_add(request:Request,cate_info: message_schema.messageCreate,
                     token : Union[str, Any] = Depends(check_jwt_token)):
    if 'token' not in request.headers:
        return JSONResponse({'code': 403, 'data': None, 'message': "用户未登录"})
    increase_dict = {'title': cate_info.title,
                     'remark': cate_info.remark,
                     'content': cate_info.content,
                     'url': cate_info.url,
                     'object': cate_info.object,
                     'token':request.headers['token']}
    result_add = curd_category.add_message(increase_dict)
    if result_add:
        return {"code": 200, "message": "新增成功", "data": None}
    else:
        return {"code": 500, "message": "操作失败", "data": None}

@router.post("/alter", summary="修改消息通知")
async def message_alter(request:Request,cate_info: message_schema.messageUpdate,
                       token : Union[str, Any] = Depends(check_jwt_token)):
    if 'token' not in request.headers:
        return JSONResponse({'code': 403, 'data': None, 'message': "用户未登录"})
    increase_dict = {'id':cate_info.id,
                     'title': cate_info.title,
                     'remark': cate_info.remark,
                     'content': cate_info.content,
                     'url': cate_info.url,
                     'object': cate_info.object}
    result_add = curd_category.update_message(increase_dict)
    if result_add:
        return {"code": 200, "message": "编辑成功", "data": None}
    else:
        return {"code": 500, "message": "操作失败", "data": None}

@router.get("/sele", summary="查询消息通知")
async def message_sele(request:Request,token : Union[str, Any] = Depends(check_jwt_token),
                      curpage: int = Query(1, ge=1, title="当前页"),
                      pagesize: int = Query(10, le=50, title="页码长度")):
    if 'token' not in request.headers:
        return JSONResponse({'code': 403, 'data': None, 'message': "用户未登录"})
    parames={'curpage':curpage,
             'pagesize':pagesize}
    result, df, df_count = curd_category.get_message(parames)
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

@router.delete("/dele", summary="删除消息通知")
async def message_dele(request:Request,cate_info:message_schema.messageDel,
                      token : Union[str, Any] = Depends(check_jwt_token)):
    if 'token' not in request.headers:
        return JSONResponse({'code': 403, 'data': None, 'message': "用户未登录"})
    #  获取传入的参数
    increase_dict = {'lists': cate_info.lists}
    result = curd_category.delete_message(increase_dict)
    if result:
        return JSONResponse({"code": 200, "message": "操作成功", "data": None})
    else:
        return JSONResponse({"code": 500, "message": "操作失败", "data": None})



