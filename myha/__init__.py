# -*- coding: utf-8 -*-
# 包构造文件，创建程序实例

import os
import sys

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import \
    SQLAlchemy  # 导入扩展类。Flask-SQLAlchemy 版本 2.4.0 Apr 25, 2019 可行

# SQLite URI 配置
WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app = Flask(__name__)
# 为了部署到线上，我添加了 wsgi.py 文件，这使得我得在 cmd 中先输入 set FLASK_APP=app.py，再输入 flask run 才能运行

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
# 注意更新这里的路径，把 app.root_path 添加到 os.path.dirname() 中
# 以便把文件定位到项目根目录
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(
    os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'my_ha_data.db')
)  # 这个在线下一用就找不到数据库的位置，添加了 'program-2022-02-02/' 后可以在线下了。但是！线上一定不能要它！！！
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

# 在扩展类实例化前加载配置
db = SQLAlchemy(app)

# 初始化 Flask-Login。用于登录
login_manager = LoginManager(app)  # 实例化扩展类


@login_manager.user_loader
def load_user(id_user):  # 创建用户加载回调函数，接受用户 ID 作为参数
    """Flask-Login 提供了一个 current_user 变量，注册这个函数的目的是，当程序运行后，如果用户已登录， current_user 变量的值会是当前用户的用户模型类记录。"""
    from myha.models import User_info
    user = User_info.query.get(int(id_user))  # 用 ID 作为 User_info 模型的主键查询对应的用户
    return user


login_manager.login_view = 'login'  # 为了让这个重定向操作正确执行，我们还需要把 login_manager.login_view 的值设为我们程序的登录视图端点（函数名），把这一行代码放到 login_manager 实例定义下面即可：
"""我不会一个 app.py 中实现即可登录“农户”，又可登录“管理员”。"""

NAME_USER = ''  # 为了“用户登录后，自动获取其 name_user”，把 name_user 传给 base.html 的“NAME_USER”，实现“定制化您好”功能


# 模板上下文处理函数
@app.context_processor
def inject_user():  # 函数名可以随意修改
    global NAME_USER
    from myha.models import User_info

    # user = User_info.query.first()  # 这里与教程不一样
    return dict(NAME_USER=NAME_USER)  # 需要返回字典，等同于 return {'user': user}


# 在构造文件 __init__.py 中，
# 为了让视图函数 routes、错误处理函数 errors 和命令函数 commands 注册到程序实例上，
#   我们需要在这里导入这几个模块。
# 但是因为这几个模块同时也要导入构造文件中的程序实例，
#   为了避免循环依赖（A 导入 B，B 导入 A），我们把这一行导入语句放到构造文件的结尾。
#   同样的，load_user() 函数和 inject_user() 函数中使用的模型类也在函数内进行导入。
# from myha import commands, errors, views  # 这条代码改一下！改成下面：
from myha import views, errors, commands

# print("跑通！\n", "os.path.dirname(app.root_path)：",
#       os.path.dirname(app.root_path))
