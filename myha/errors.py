# -*- coding: utf-8 -*-
# 错误处理函数

from flask import render_template

from myha import app


# 400 错误处理函数
@app.errorhandler(400)
def bad_request(e):
    return render_template('errors/400.html'), 400


# 404 错误处理函数
@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    # user_info = User_info.query.first()  # 被删掉是因为有了模板上下文处理函数 inject_user()
    return render_template('errors/404.html'), 404  # 返回模板和状态码

# 500 错误处理函数
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500