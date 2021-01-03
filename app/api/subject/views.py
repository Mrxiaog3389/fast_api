# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 10:40
# @Author  : Xiaoyunlong
from fastapi import APIRouter,Form,Body,Path,Header,Query,Request
from fastapi.responses import JSONResponse
import json,math,warnings
from app.common.logger import *
from .schemas import category_schema
from .crud.category import curd_category

#过滤掉警告
warnings.filterwarnings('ignore')

router = APIRouter()

@router.post("/insert", summary="新增题库分类")
async def subject_add(cate_info: category_schema.CategoryCreate,request: Request):
    logging.info(f"添加分类->分类名:{cate_info.class_name}")
    increase_dict = {'class_name': cate_info.class_name,
                     'admin_id': cate_info.admin_id,
                     'appcode': cate_info.appcode,
                     'user-agent':request}
    result_add = curd_category.add_subject(increase_dict)
    if result_add:
        return {"code": 200, "message": "新增成功", "data": None}
    else:
        return {"code": 500, "message": "操作失败", "data": None}

@router.post("/alter", summary="编辑题库分类")
async def subject_alter(cate_info: category_schema.CategoryUpdate):
    logging.info(f"修改分类->分类id:{cate_info.class_id}")
    increase_dict = {'class_name': cate_info.class_name,
                     'class_id':cate_info.class_id,
                     'uadmin_id': cate_info.admin_id}
    ae_classify='ae_classify'
    result_add = curd_category.update_cate(ae_classify,increase_dict)
    if result_add:
        return {"code": 200, "message": "编辑成功", "data": None}
    else:
        return {"code": 500, "message": "操作失败", "data": None}

@router.get("/sele", summary="查询题库分类")
async def subject_sele(is_all:int=None):
    return_dict = {'code': 200, 'message': 'ok', 'data': None}
    sql_statce, sql,res = curd_category.get_all_count_num()
    if is_all == 1:
        if len(sql) !=0 and sql_statce:
            return_dict['data']=sql.to_dict(orient='records')
            return JSONResponse(return_dict)
        else:
            return JSONResponse(return_dict)
    else:
        if len(sql) !=0 and sql_statce:
            return_dict['data'] = sql.to_dict(orient='records')
            if '0' in res[res['class_id'] == 0]['class_id'].tolist():
                return_dict['data'].append({"class_id": res[res['class_id'] == 0]['class_id'].tolist()[0],
                                            "class_name": "未分类",
                                            'count_num':res[res['class_id'] == 0]['count_num'].tolist()[0]})
                return JSONResponse(return_dict)
            else:
                return_dict['data'].append({"class_id": 0,
                                            "class_name": "未分类",
                                            'count_num': 0})
                return JSONResponse(return_dict)
        else:
            return JSONResponse(return_dict)

@router.delete("/dele", summary="删除题库分类")
async def subject_dele(cate_info:category_schema.CategoryDel):
    #  获取传入的参数
    ae_classify = 'ae_classify'
    results, results_df = curd_category.get_all(ae_classify)
    uuid = results_df['class_id'].tolist()
    class_id_dict={}
    if cate_info.class_id in uuid:
        class_id_dict['class_id']=cate_info.class_id
        classid='class_id'
        results = curd_category.remove(ae_classify,classid,class_id_dict)
        if results:
            return JSONResponse({"code": 200, "message": "删除成功", "data": None})
        else:
            return JSONResponse(json.dumps({"code": 500, "message": "操作失败", "data": None}))
    else:
        return JSONResponse(json.dumps({"code": 500, "message": "删除的题库不存在", "data": None}))

@router.get("/questionlist", summary="获取题目列表")
async def question_sele(class_id:int=None,
                        question_type:str=None,
                        question_title:str=None,
                        curpage: int = Query(1, ge=1, title="当前页"),
                        pagesize: int = Query(10, le=50, title="页码长度")):
    parames={'curpage':curpage,
             'pagesize':pagesize,
             'class_id':class_id,
             'question_type':question_type,
             'question_title':question_title}
    return_dict = {'code': 200, 'message': 'ok', 'data': {'page_count':None,'total_num':None,'list': None}}
    df, df_count = curd_category.get_question_list(parames)
    if parames['question_title'] != None:
        return_dict['data']['total_num'] = df_count
        return_dict['data']['list'] = df
    else:
        return_dict['data']['total_num']=df_count
        return_dict['data']['list'] = df.to_dict(orient='records')
    if df_count == 0:
        return_dict['data']['page_count'] = 0
        return JSONResponse(return_dict)
    elif df_count / pagesize < 1:
        return_dict['data']['page_count'] = 1
        return JSONResponse(return_dict)
    else:
        return_dict['data']['page_count'] = math.floor(df_count / pagesize) + 1
        return JSONResponse(return_dict)

@router.get("/detailslist", summary="获取题目详情")
async def question_details(question_id:int):
    parames={'question_id':question_id}
    return_dict = {'code': 200, 'message': 'ok', 'data': None}
    sql = curd_category.get_details_list(parames)
    ae_classify = 'ae_classify'
    results, results_df = curd_category.get_all(ae_classify)
    for i in sql:
        dic={}
        dic['analysis'] = i[0]
        dic['class_id'] = i[1]
        dic['class_name'] = results_df[results_df['class_id']==i[1]]['class_name'].tolist()[0]
        dic['correct_option'] = i[2]
        dic['options'] = json.loads(i[3])
        dic['question_id'] = i[4]
        dic['question_title'] = i[5]
        dic['question_type'] = i[6]
        return_dict['data'] = dic
    return JSONResponse(return_dict)

@router.post("/questiontran", summary="转移题")
async def question_transfer(cate_info: category_schema.Questiontransfer):
    logging.info(f"修改分类->分类id:{cate_info.class_id}")
    increase_dict = {'question_id': cate_info.question_id,
                     'class_id':cate_info.class_id,
                     'uadmin_id': cate_info.admin_id}
    ae_questions='ae_questions'
    result_add = curd_category.update_question(ae_questions,increase_dict)
    if result_add:
        return {"code": 200, "message": "转移成功", "data": None}
    else:
        return {"code": 500, "message": "操作失败", "data": None}

@router.delete("/questiondele", summary="删除题")
async def question_dele(cate_info:category_schema.QuestionDel):
    #  获取传入的参数
    class_id_dict={}
    class_id_dict['question_id']=cate_info.question_id
    results = curd_category.remove_question(class_id_dict)
    if results:
        return JSONResponse({"code": 200, "message": "删除成功", "data": None})
    else:
        return JSONResponse(json.dumps({"code": 500, "message": "操作失败", "data": None}))