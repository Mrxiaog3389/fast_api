from fastapi import APIRouter,Form,Body,Path,Header,Query,Request
from fastapi.responses import JSONResponse
import json,math,warnings
from app.common.logger import *
from .schemas import test_schema
from .crud.test import curd_category
import numpy as np
router = APIRouter()

#过滤掉警告
warnings.filterwarnings('ignore')

@router.post("/insert", summary="添加考试分类")
async def subject_add(cate_info: test_schema.testCreate,request: Request):
    logging.info(f"添加分类->分类名:{cate_info.class_name}")
    increase_dict = {'class_name': cate_info.class_name,
                     'admin_id': cate_info.admin_id,
                     'appcode': cate_info.appcode,
                     'user_agent':request}
    result_add = curd_category.add_test(increase_dict)
    if result_add:
        return {"code": 200, "message": "新增成功", "data": None}
    else:
        return {"code": 500, "message": "操作失败", "data": None}

@router.post("/alter", summary="编辑考试分类")
async def subject_alter(cate_info: test_schema.testUpdate):
    logging.info(f"修改分类->分类id:{cate_info.class_id}")
    increase_dict = {'class_name': cate_info.class_name,
                     'class_id':cate_info.class_id,
                     'uadmin_id': cate_info.admin_id}
    ae_classify='ae_classify'
    result_add = curd_category.update_test(ae_classify,increase_dict)
    if result_add:
        return {"code": 200, "message": "编辑成功", "data": None}
    else:
        return {"code": 500, "message": "操作失败", "data": None}

@router.get("/sele", summary="获取考试分类列表")
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
        if len(sql) != 0 and sql_statce:
            return_dict['data'] = sql.to_dict(orient='records')
            if '0' in res[res['class_id'] == 0]['class_id'].tolist():
                return_dict['data'].append({"class_id": res[res['class_id'] == 0]['class_id'].tolist()[0],
                                            "class_name": "未分类",
                                            'count_num': res[res['class_id'] == 0]['count_num'].tolist()[0]})
                return JSONResponse(return_dict)
            else:
                return_dict['data'].append({"class_id": 0,
                                            "class_name": "未分类",
                                            'count_num': 0})
                return JSONResponse(return_dict)
        else:
            return JSONResponse(return_dict)

@router.delete("/dele", summary="删除考试分类")
async def subject_dele(cate_info:test_schema.testDel):
    #  获取传入的参数
    ae_classify = 'ae_classify'
    results, results_df = curd_category.get_all(ae_classify)
    uuid = results_df['class_id'].tolist()
    class_id_dict={}
    if cate_info.class_id in uuid:
        class_id_dict['class_id']=cate_info.class_id
        results = curd_category.remove(class_id_dict)
        if results:
            return JSONResponse({"code": 200, "message": "删除成功", "data": None})
        else:
            return JSONResponse(json.dumps({"code": 500, "message": "操作失败", "data": None}))
    else:
        return JSONResponse(json.dumps({"code": 500, "message": "删除的题库不存在", "data": None}))

@router.delete("/testpaperDele", summary="删除试卷")
async def subject_dele(cate_info:test_schema.testpaperDel):
    #  获取传入的参数
    class_id_dict={}
    class_id_dict['exam_id']=cate_info.exam_id
    results = curd_category.remove_test(class_id_dict)
    if results:
        return JSONResponse({"code": 200, "message": "删除成功", "data": None})
    else:
        return JSONResponse(json.dumps({"code": 500, "message": "操作失败", "data": None}))


@router.delete("/Release", summary="发布考试")
async def subject_dele(cate_info:test_schema.Release):
    #  获取传入的参数
    ae_classify='ae_exam'
    class_id_dict={}
    class_id_dict['exam_id']=cate_info.exam_id
    results = curd_category.update_Release(ae_classify,class_id_dict)
    if results:
        return JSONResponse({"code": 200, "message": "发布成功", "data": None})
    else:
        return JSONResponse(json.dumps({"code": 500, "message": "操作失败", "data": None}))

@router.get("/testlist", summary="获取试卷列表")
async def question_sele(class_id:int=None,
                        name:str=None,
                        curpage: int = Query(1, ge=1, title="当前页"),
                        pagesize: int = Query(10, le=50, title="页码长度")):
    parames={'curpage':curpage,
             'pagesize':pagesize,
             'class_id':class_id,
             'name':name}
    return_dict = {'code': 200, 'message': 'ok', 'data': {'page_count':None,'total_num':None,'list': None}}
    df, df_count = curd_category.get_test_list(parames)
    if parames['class_id'] != None or parames['name'] != None:
        return_dict['data']['total_num']=df_count
        return_dict['data']['list'] = df
    else:
        return_dict['data']['total_num'] = df_count
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

@router.get("/detailslist", summary="获取试卷详情")
async def question_details(exam_id:int):
    parames={'exam_id':exam_id}
    return_dict = {'code': 200, 'message': 'ok', 'data': None}
    sql,sql1 = curd_category.get_details_test_list(parames)
    ae_classify = 'ae_classify'
    results, results_df = curd_category.get_all(ae_classify)
    li=[]
    dic={}
    dic['class_id'] = sql[0][0]
    dic['name'] = sql[0][1]
    dic['img'] = sql[0][2]
    dic['intro'] = sql[0][3]
    dic['answer_show'] = sql[0][4]
    dic['publish_status'] = sql[0][5]
    dic['class_name'] = results_df[results_df['class_id'] == sql[0][0]]['class_name'].tolist()[0]
    dic['question_count'] = len(sql1)
    dic['questions'] = []
    for j in sql1:
        dic1={}
        li.append(j[7])
        dic1['exam_question_id'] = j[0]
        dic1['serial_num'] = j[1]
        dic1['question_type'] = j[2]
        dic1['question_title'] = j[3]
        dic1['options'] = json.loads(j[4])
        dic1['correct_option'] = j[5]
        dic1['analysis'] = j[6]
        dic1['score'] = j[7]
        dic['questions'].append(dic1)
    dic['total_score'] = sum(li)
    return_dict['data']=dic
    return JSONResponse(return_dict)

@router.get("/review", summary="批阅查看")
async def review(member_exam_id: int):
    parames = {'member_exam_id': member_exam_id}
    return_dict = {'code': 200, 'message': 'ok', 'data': None}
    if curd_category.get_review(parames) == False:
        return JSONResponse(return_dict)
    else:
        df_user = curd_category.get_user_list()
        sql,sql1,sql2=curd_category.get_review(parames)
        dic = {}
        dic['exam_id'] = sql[0][1]
        dic['exam_time'] = sql[0][7]
        dic['false_num'] = sql[0][5]
        dic['grade'] = sql[0][3]
        dic['itime'] = sql[0][8]
        dic['member_avatar'] = df_user[df_user['member_id'] == sql[0][2]]['wx_headimgurl'].tolist()[0]
        dic['member_exam_id'] = sql[0][0]
        dic['member_id'] = sql[0][2]
        dic['member_name'] = df_user[df_user['member_id'] == sql[0][2]]['member_name'].tolist()[0]
        dic['not_num'] = sql[0][6]
        dic['questions'] = []
        dic['true_num'] = sql[0][4]
        for i in range(len(sql2)):
            dic1={}
            dic1['exam_question_id'] = sql2[i][0]
            dic1['serial_num'] = sql2[i][1]
            dic1['question_type'] = sql2[i][2]
            dic1['question_title'] = sql2[i][3]
            dic1['correct_option'] = sql2[i][4]
            dic1['analysis'] = sql2[i][5]
            dic1['options'] = json.loads(sql2[i][6])
            dic1['answer_option']=sql1[i][0]
            dic['questions'].append(dic1)
            return_dict['data'] = dic
        return JSONResponse(return_dict)


@router.get("/reviewlist", summary="批阅列表")
async def review_list(exam_id:int,
                        member_name:str=None,
                        curpage: int = Query(1, ge=1, title="当前页"),
                        pagesize: int = Query(10, le=50, title="页码长度")):
    parames={'curpage':curpage,
             'pagesize':pagesize,
             'exam_id':exam_id,
             'member_name':member_name}
    return_dict = {'code': 200, 'message': 'ok', 'data': {'page_count':None,'total_num':None,'list':None}}
    df,df_count=curd_category.get_review_list(parames)
    # return_dict['data']['total_num']=df_count
    if df_count == 0:
        return_dict['data']['page_count'] = 0
        return JSONResponse(return_dict)
    elif df_count / pagesize < 1:
        return_dict['data']['page_count'] = 1
        df_user = curd_category.get_user_list()
        list = []
        for i in df:
            dic = {}
            dic['exam_id'] = i[0]
            dic['grade'] = i[1]
            dic['is_remark'] = 1
            dic['itime'] = i[2]
            dic['member_avatar'] = df_user[df_user['member_id'] == i[4]]['wx_headimgurl'].tolist()[0]
            dic['member_exam_id'] = i[3]
            dic['member_id'] = i[4]
            dic['member_name'] = df_user[df_user['member_id'] == i[4]]['member_name'].tolist()[0]
            dic['remark_admin_name'] = '--'
            list.append(dic)
        return_dict['data']['list'] = list
        return JSONResponse(return_dict)
    else:
        df_user = curd_category.get_user_list()
        list=[]
        for i in df:
            dic={}
            dic['exam_id']=i[0]
            dic['grade'] = i[1]
            dic['is_remark'] =1
            dic['itime'] = i[2]
            dic['member_avatar'] = df_user[df_user['member_id'] == i[4]]['wx_headimgurl'].tolist()[0]
            dic['member_exam_id'] = i[3]
            dic['member_id'] = i[4]
            dic['member_name'] = df_user[df_user['member_id'] == i[4]]['member_name'].tolist()[0]
            dic['remark_admin_name'] = '--'
            list.append(dic)
        return_dict['data']['list'] = list
        return_dict['data']['page_count'] = math.floor(df_count / pagesize) + 1
        return JSONResponse(return_dict)