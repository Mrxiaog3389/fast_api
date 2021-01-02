from fastapi import APIRouter,Depends,Request,Query
from fastapi.responses import JSONResponse
import json,math,warnings
from app.common.logger import *
from .schemas import project_schema
from .crud.project import curd_category,find
from app.core.security import check_jwt_token
from app.utils.exsel_tools import ExcelTools

from typing import Any, Union
from datetime import datetime
from fastapi.responses import StreamingResponse
import mimetypes

router = APIRouter()

#过滤掉警告
warnings.filterwarnings('ignore')

@router.get("/select", summary="项目查询")
async def project_select(status:int,
                         curpage: int = Query(1, ge=1, title="当前页"),
                         pagesize: int = Query(10, le=50, title="页码长度"),
                         token : Union[str, Any] = Depends(check_jwt_token)):
    req_dict = {'token':token,
                'status': status,
                'curpage': curpage,
                'pagesize': pagesize}
    result, df, df_count = curd_category.project_select(req_dict)
    return_dict = {'code': 200, 'message': '操作成功', 'data': {'page_count': None, 'total_num': None, 'list': None}}
    if result and df_count == 0:
        return_dict['data']['page_count'] = 0
        return_dict['data']['total_num'] = 0
        return JSONResponse(return_dict)
    elif result and df_count / int(pagesize) < 1:
        return_dict['data']['page_count'] = 1
        return_dict['data']['total_num'] = df_count
        return_dict['data']['list'] = df[(curpage-1)*10:pagesize]
        return JSONResponse(return_dict)
    elif result:
        return_dict['data']['page_count'] = math.floor(df_count / int(pagesize)) + 1
        return_dict['data']['total_num'] = df_count
        return_dict['data']['list'] = df[(curpage-1)*10:pagesize]
        return JSONResponse(return_dict)
    else:
        return JSONResponse({"code": 500, "message": "操作失败", "data": None})

@router.get("/proceselect", summary="进度查询")
async def prosess_select(prono:str):
    req_dict = {'prono': prono}
    result, dic = curd_category.prosess_select(req_dict)
    return_dict = {'code': 200, 'message': '操作成功', 'data': None}
    if result:
        return_dict['data'] = dic
        return JSONResponse(return_dict)
    else:
        return JSONResponse(return_dict)

@router.get("/export", summary="导出")
async def excel_export(token : Union[str, Any] = Depends(check_jwt_token)):
    req_dict = {'token': token}
    rows,columns = find(req_dict)
    if rows:
        excel_tools = ExcelTools()
        excel = excel_tools.dict_to_excel(rows,columns)
        file_name = 'devices' + '-' + datetime.now().strftime("%Y%m%d_%H%M%S") + '.xlsx'
        mime = mimetypes.guess_type(file_name)[0]
        return StreamingResponse(content=excel,
                                 media_type=mime,
                                 headers={'Content-Disposition': 'filename="%s"' % file_name})