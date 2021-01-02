from fastapi import APIRouter,Query
from fastapi.responses import JSONResponse
import warnings
from app.common.logger import *
from app.core.security import create_access_token
from .schemas import user_schema
from .crud.user import curd_category
from datetime import timedelta
import hashlib,math
#过滤掉警告
warnings.filterwarnings('ignore')
router = APIRouter()


@router.post("/login", summary="登录")
async def login(user_info: user_schema.UserInfo):
    increase_dict = {'username': user_info.username,
                     'password': user_info.password}
    password = hashlib.md5(increase_dict['password'].encode())
    return_dict = {'code': 200, 'message': 'ok', 'data': None}
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    if curd_category.login(increase_dict)==False:
        return {"code": 500, "message": "操作失败", "data": None}
    else:
        df, sql_username_list=curd_category.login(increase_dict)
        list=[]
        for i in sql_username_list['username'].values.tolist():
            list.append(i)
        if increase_dict['username'] in list:
            if password.hexdigest() == df[0][2]:
                return_dict['data']={'user_id':df[0][0]}
                return_dict['token']=create_access_token(increase_dict['username'], expires_delta=access_token_expires)
                return JSONResponse(return_dict)
            else:
                return {"code": 403, "message": "密码错误", "data": None}
        else:
            return {"code": 403, "message": "用户名错误", "data": None}

@router.get('/select',summary="用户查询")
async def user_select(curpage: int = Query(1, ge=1, title="当前页"),
                pagesize: int = Query(10, le=50, title="页码长度")):
    req_dict = {'curpage':curpage,'pagesize':pagesize}
    result,df, df_count = curd_category.userlist(req_dict)

    return_dict = {'code': 200, 'message': '操作成功', 'data': {'page_count':None,'total_num':None,'list': None}}
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
        return_dict['data']['list']=df
        return JSONResponse(return_dict)
    else:
        return JSONResponse({"code": 500, "message": "操作失败", "data": None})

@router.post("/register",summary="用户注册")
async def user_register(user_info: user_schema.Userregister):
    parames = {'username': user_info.username,
               'password': user_info.password,
               'password2': user_info.password2,
               'nick_name': user_info.nick_name,
               'face_img': user_info.face_img}
    # 校验参数
    if not all([parames['username'],parames['password'], parames['password2']]):
        return JSONResponse({"code": 506, "message": "参数不完整", "data": None})
    if parames['password'] != parames['password2']:
        return JSONResponse({"code": 407, "message": "两次密码不一致", "data": None})

    #判断用户的手机号是否注册过
    result,user=curd_category.get_userid()
    userlist=user['username'].tolist()
    if parames['username'] in userlist:
        # 表示手机号已存在
        return JSONResponse({"code": 408, "message": "用户已存在", "data": None})
    result_add=curd_category.useregister(parames)
    if result_add:
        return JSONResponse({"code": 200, "message": "操作成功", "data": None})
    else:
        return JSONResponse({"code": 500, "message": "操作失败", "data": None})

@router.put("/alter",summary="用户修改")
async def user_alter(user_info: user_schema.Useralter):
    parames = {'id':user_info.id,
               'username': user_info.username,
               'password': user_info.password,
               'password2': user_info.password2,
               'nick_name': user_info.nick_name,
               'face_img': user_info.face_img,
               'roleIds': user_info.roleIds}
    # 校验参数
    if parames['password'] != parames['password2']:
        return JSONResponse({"code": 407, "message": "两次密码不一致", "data": None})

    result_alter = curd_category.useralter(parames)
    if result_alter:
        return JSONResponse({"code": 200, "message": "操作成功", "data": None})
    else:
        return JSONResponse({"code": 500, "message": "操作失败", "data": None})

@router.delete('/dele',summary="用户删除")
async def user_dele(user_info: user_schema.Userdele):
    """用户删除接口"""
    #  获取传入的参数
    parames = {'id': user_info.id}
    result, user = curd_category.get_userid()
    userlist = user['id'].tolist()
    for r in parames['id']:
        if r in userlist:
            result_dele=curd_category.userdele(parames)
            if result_dele:
                return JSONResponse({"code": 200, "message": "操作成功", "data": None})
            else:
                return JSONResponse({"code": 500, "message": "操作失败", "data": None})
        else:
            return JSONResponse({"code": 409, "message": "删除的用户不存在", "data": None})

@router.get('/control',summary="用户权限查询")
async def control_select():
    """用户权限查询接口"""
    return_dict = {'code': '200', 'message': '操作成功','data':{'list':None}}
    result, df = curd_category.usercontrol()
    if result:
        if len(df) != 0:
            return_dict['data']['list'] = df.to_dict(orient='records')
            return JSONResponse(return_dict)
        else:
            return JSONResponse(return_dict)
    else:
        return JSONResponse({"code": 500, "message": "操作失败", "data": None})

@router.post('/password',summary="密码修改")
async def alter_password(user_info: user_schema.Userpassword):
    # 获取请求的json数据，返回字典
    parames = {'userId': user_info.userId,
               'newPwd': user_info.newPwd,
               'oldPwd': user_info.oldPwd}
    # 校验参数
    if not all([parames['userId'],parames['newPwd'],parames['oldPwd']]):
        return JSONResponse({"code": 506, "message": "参数不完整", "data": None})
    result = curd_category.alterpasswors(parames)
    if result:
        return JSONResponse({"code": 200, "message": "操作成功", "data": None})
    else:
        return JSONResponse({"code": 500, "message": "操作失败", "data": None})

@router.get("/information",summary="个人信息查询")
async def user_information(userid:str):
    req_dict={"userid":userid}
    result,dic = curd_category.user_information(req_dict)
    return_dict = {'code': 200, 'message': '操作成功', 'data': None}
    if result:
        return_dict['data'] = dic
        return JSONResponse(return_dict)
    else:
        return JSONResponse({"code": 500, "message": "操作失败", "data": None})

@router.put("/alterinformation",summary="个人信息修改")
async def user_alterinformation(user_info: user_schema.Useralterinformation):
    parames = {'userId': user_info.userId,
               'username': user_info.username,
               'nick_name': user_info.nick_name,
               'face_img': user_info.face_img}
    result = curd_category.user_alterinformation(parames)
    if result:
        return JSONResponse({"code": 200, "message": "操作成功", "data": None})
    else:
        return JSONResponse({"code": 500, "message": "操作失败", "data": None})

@router.get('/roleselect',summary="角色查询")
async def role_select():
    """角色列表查询接口"""
    return_dict = {'code': '200', 'message': '操作成功','data':{'list':None}}
    result, df = curd_category.role_select()
    if result:
        if len(df) != 0:
            return_dict['data']['list'] = df.to_dict(orient='records')
            return JSONResponse(return_dict)
        else:
            return JSONResponse(return_dict)
    else:
        return JSONResponse({"code": 500, "message": "操作失败", "data": None})

@router.delete('/roledele',summary="角色删除")
async def role_dele(user_info: user_schema.roledele):
    """角色删除接口"""
    #  获取传入的参数
    parames = {'id': user_info.id}
    result, user = curd_category.get_roleid()
    rolelist = user['id'].tolist()
    for r in parames['id']:
        if r in rolelist:
            result_dele = curd_category.roledele(parames)
            if result_dele:
                return JSONResponse({"code": 200, "message": "操作成功", "data": None})
            else:
                return JSONResponse({"code": 500, "message": "操作失败", "data": None})
        else:
            return JSONResponse({"code": 409, "message": "删除的角色不存在", "data": None})

@router.post('/roleincrease',summary="角色新增")
async def role_increase(user_info: user_schema.roleincrease):
    """角色新增接口"""
    #  获取传入的参数
    parames = {'description': user_info.description,
               'resourceList': user_info.resourceList}
    # 校验参数
    if not all([parames['description']]):
        return JSONResponse({"code": 506, "message": "参数不完整", "data": None})
    result_add = curd_category.roleincrease(parames)
    if result_add:
        return JSONResponse({"code": 200, "message": "操作成功", "data": None})
    else:
        return JSONResponse({"code": 500, "message": "操作失败", "data": None})

@router.put('/rolealter',summary="角色修改")
async def role_alter(user_info: user_schema.rolealter):
    """角色修改接口"""
    #  获取传入的参数
    parames = {'id':user_info.id,
               'description': user_info.description,
               'resourceList': user_info.resourceList}
    # 校验参数
    if not all([parames['id'], parames['description']]):
        return JSONResponse({"code": 506, "message": "参数不完整", "data": None})
    result_alter = curd_category.rolealter(parames)
    if result_alter:
        return JSONResponse({"code": 200, "message": "操作成功", "data": None})
    else:
        return JSONResponse({"code": 500, "message": "操作失败", "data": None})

@router.get('/roleresourcequery',summary="查询角色所属的权限")
async def resource_query(id:str):
    #  获取传入的参数
    req_dict={"id":id}
    result,df = curd_category.role_query(req_dict)
    return_dict = {'code': 200, 'message': '操作成功', 'data': {'list':None}}
    if result:
        return_dict['data']['list'] = df
        return JSONResponse(return_dict)
    else:
        return JSONResponse(return_dict)

@router.get('/resourceselect',summary="权限查询")
async def resource_select():
    """权限列表查询接口"""
    result, lis=curd_category.resource_select()
    return_dict = {'code': 200,'message': '操作成功','data':None}
    return_dict['data']=lis
    return JSONResponse(return_dict)

@router.post("/resourceinsert",summary="权限新增")
async def resource_insert(user_info: user_schema.resourceincrease):
    #获取请求的json数据，返回字典
    parames = {'groupName': user_info.groupName,
               'name': user_info.name,
               'method': user_info.method,
               'uri': user_info.uri}
    # 校验参数
    if not all([parames['groupName'],parames['name'], parames['method'],parames['uri']]):
        return JSONResponse({"code": 506, "message": "参数不完整", "data": None})
    result_add = curd_category.resourceincrease(parames)
    if result_add:
        return JSONResponse({"code": 200, "message": "操作成功", "data": None})
    else:
        return JSONResponse({"code": 500, "message": "操作失败", "data": None})

@router.put("/resourcealter",summary="权限修改")
async def resource_alter(user_info: user_schema.resourcealter):
    parames = {'id': user_info.id,
               'name': user_info.name,
               'method': user_info.method,
               'uri': user_info.uri}
    # 校验参数
    if not all([parames['name'],parames['method'],parames['uri']]):
        return JSONResponse({"code": 506, "message": "参数不完整", "data": None})
    result_alter = curd_category.resourcealter(parames)
    if result_alter:
        return JSONResponse({"code": 200, "message": "操作成功", "data": None})
    else:
        return JSONResponse({"code": 500, "message": "操作失败", "data": None})

@router.delete('/resourcedele',summary="权限删除")
async def resource_dele(user_info: user_schema.resourcedele):
    #  获取传入的参数
    parames = {'id': user_info.id}
    result, user = curd_category.get_resource()
    resourcelist = user['id'].tolist()
    list = [int(x) for x in resourcelist]
    for r in parames['id']:
        if r in list:
            result_dele = curd_category.resourcedele(parames)
            if result_dele:
                return JSONResponse({"code": 200, "message": "操作成功", "data": None})
            else:
                return JSONResponse({"code": 500, "message": "操作失败", "data": None})
        else:
            return JSONResponse({"code": 409, "message": "删除的权限不存在", "data": None})

# @router.post("/login", summary="登录")
# async def login(user_info: user_schema.UserInfo):
#     increase_dict = {'username': user_info.username,
#                      'password': user_info.password}
#     password = hashlib.md5(increase_dict['password'].encode())
#     return_dict = {'code': 200, 'message': 'ok', 'data': None}
#     access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
#     if curd_category.login(increase_dict)==False:
#         return {"code": 500, "message": "操作失败", "data": None}
#     else:
#         df, sql_username_list=curd_category.login(increase_dict)
#         list=[]
#         for i in sql_username_list['username'].values.tolist():
#             list.append(str(i, encoding = "utf8"))
#         if increase_dict['username'] in list:
#             if password.hexdigest() == df[0][0]:
#                 return_dict['data']={'admin_id':df[0][1],
#                                      'img':df[0][2],
#                                      'key':df[0][3],
#                                      'username':str(df[0][4], encoding = "utf8")}
#                 return_dict['token']=create_access_token(increase_dict['username'], expires_delta=access_token_expires)
#                 return JSONResponse(return_dict)
#             else:
#                 return {"code": 403, "message": "密码错误", "data": None}
#         else:
#             return {"code": 403, "message": "用户名错误", "data": None}
#
#
# @router.get("/log/info", summary="获取登录日志")
# async def login_sele(request: Request,username:str=None,
#                      startingtime:str=None,
#                      endtime:str=None,
#                      curpage: int = Query(1, ge=1, title="当前页")):
#     parames={'username':username,
#              'startingtime':startingtime,
#              'endtime':endtime,
#              'curpage':curpage}
#     return_dict = {'code': 200, 'message': 'ok', 'data': {'page_count':None,'total_num':None,'list': None}}
#     ip = request.client.host
#     node = uuid.getnode()
#     macHex = uuid.UUID(int=node).hex[-12:]
#     mac = []
#     for i in range(len(macHex))[::2]:
#         mac.append(macHex[i:i + 2])
#     mac = ':'.join(mac)
#     print('MAC:', mac)
#     print(socket.getfqdn(socket.gethostname()))
#     print(socket.gethostbyname(socket.gethostname()))
#     print(ip)
#     print(request.headers['user-agent'])
#
#     print(request.url)
#     print(request.base_url)
#     print(request.url.path)
#
#
#
#     df,df_count=curd_category.get_log_list(parames)
#     return_dict['data']['total_num'] = df_count
#     return_dict['data']['list'] = df
#     return_dict['data']['page_count'] = math.floor(df_count / 30) + 1
#     if df_count == 0:
#         return_dict['data']['page_count'] = 0
#         return JSONResponse(return_dict)
#     elif df_count / 30 < 1:
#         return_dict['data']['page_count'] = 1
#         return JSONResponse(return_dict)
#     else:
#         return_dict['data']['page_count'] = math.floor(df_count / 30) + 1
#         return JSONResponse(return_dict)
#
# @router.get("/manager/selectlist", summary="管理员列表")
# async def admin_sele(tel:str=None,
#                      status:str=None,
#                      role_id:str=None,
#                      curpage: int = Query(1, ge=1, title="当前页数"),
#                      pagesize:int = Query(10, le=50, title="每页显示条数")):
#     parames={'tel':tel,
#              'status':status,
#              'role_id':role_id,
#              'curpage':curpage,
#              'pagesize':pagesize}
#     return_dict = {'code': 200, 'message': 'ok', 'data': {'page_count':None,'total_num':None,'list': None}}
#
#     df,df_count=curd_category.get_admin_list(parames)
#     return_dict['data']['total_num'] = df_count
#     return_dict['data']['list'] = df
#     if df_count == 0:
#         return_dict['data']['page_count'] = 0
#         return JSONResponse(return_dict)
#     elif df_count / 30 < 1:
#         return_dict['data']['page_count'] = 1
#         return JSONResponse(return_dict)
#     else:
#         return_dict['data']['page_count'] = math.floor(df_count / 30) + 1
#         return JSONResponse(return_dict)
#
# @router.get("/alter/password", summary="修改密码")
# async def admin_password(old_password:str,
#                      username:str,
#                      new_password:str):
#     m = hashlib.md5(old_password.encode())
#     n=hashlib.md5(new_password.encode())
#     parames={'old_password':m.hexdigest(),
#              'username':username,
#              'new_password':n.hexdigest()}
#     return_dict = {'code': 200, 'message': 'ok'}
#     result=curd_category.alter_password(parames)
#     if type(result) == str:
#         return_dict['message']=result
#         return JSONResponse(return_dict)
#     else:
#         return JSONResponse({'code': 200, 'message': 'ok', 'data': '修改成功'})
#
# @router.get("/alter/data", summary="修改资料")
# async def admin_data(img:str,admin_id:int):
#     parames={'img':img,
#              'admin_id':admin_id}
#     result=curd_category.alter_data(parames)
#     if result:
#         return JSONResponse({'code': 200, 'message': 'ok', 'data': '修改成功'})
#     else:
#         return JSONResponse({'code': 200, 'message': 'ok', 'data': '修改失败'})