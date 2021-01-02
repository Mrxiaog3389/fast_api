# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 10:40
# @Author  : Xiaoyunlong
from fastapi import FastAPI,Request, status
from app.api import api_router
from app.setting import main_init
from app.common import logger
from fastapi.middleware.cors import CORSMiddleware
# from aioredis import create_redis_pool
config = main_init.Init_Config('192.168.4.131','app.exam','root','123456!@#')


def create_app():
    app = FastAPI(
        title="FastAPI",
        description="url: http://127.0.0.1:8081/docs#/ ",
        version="0.1.1")
    app.include_router(api_router,prefix="/api")  # 注册路由
    register_cors(app)  # 跨域设置
    # register_redis(app)  # 挂载redis

    return app

def register_cors(app: FastAPI):
    """
    支持跨域
    :param app:
    :return:
    """

    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex='https?://.*',  # 改成用正则就行了
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# def register_redis(app: FastAPI) -> None:
#     """
#     把redis挂载到app对象上面
#     :param app:
#     :return:
#     """
#
#     @app.on_event('startup')
#     async def startup_event():
#         """
#         获取链接
#         :return:
#         """
#         app.state.redis = await create_redis_pool(config.rediurl)
#
#     @app.on_event('shutdown')
#     async def shutdown_event():
#         """
#         关闭
#         :return:
#         """
#         app.state.redis.close()
#         await app.state.redis.wait_closed()


