这是一个基于fast_api编写的后端接口项目

包括常用的增删改查接口、导出接口、登陆接口


环境安装
pip install -r requirements.txt

本地测试
# 命令行输入
uvicorn main:app --host 0.0.0.0
# 浏览器访问
http://127.0.0.1:8000/docs
