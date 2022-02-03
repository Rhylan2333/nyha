# -*- coding: utf-8 -*-
# 视图函数
from datetime import date

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from myha import app, db, formula
from myha.models import Admin_info, Area_info, Ha_info, User_info

y0 = ''
y00 = ''
id_user = ''
id_area = ''
NAME_USER = ''
list_area_name_area = []  # 虽然说每次查询前都要清空，但……这里会不会出现“头咬尾巴”的情况啊
list_area_admin_id_area = []


@app.route('/', methods=['GET', 'POST'])
def index():
    global y0, y00, NAME_USER
    if request.method == 'POST':  # 判断是否是 POST 请求
        if not current_user.is_authenticated:  # 如果当前用户未认证，则 ta 只能使用“计算”功能
            """
            is_authenticated 的说明 见 Class User_info...
            创建新条目的操作稍微有些不同，
            因为对应的 '/' 视图同时处理显示页面的 GET 请求和创建新条目的 POST 请求，
            我们仅需要禁止未登录用户创建新条目，
            因此不能使用 login_required，而是在函数内部的 POST 请求处理代码前进行过滤：
            """
            x1 = request.form.get('x1')  # 传入表单对应输入字段的 name 值
            x2 = request.form.get('x2')
            # 验证数据
            if not x1 or not x2:
                flash('Invalid input.')  # 显示错误提示
                return redirect(url_for('index'))  # 重定向回主页
            else:
                try:
                    """防止输入非数字报错"""
                    y00 = formula.cal_the_complex_of_1_and_2_generation_of_Ha_0(
                        eval(x1) / 50,
                        eval(x2) / 300)
                    return redirect(url_for('index'))  # 重定向回主页
                except:
                    flash('请重新输入，不要输入非数字内容！')  # 显示错误提示
                    return redirect(url_for('index'))  # 重定向回主页

        # 获取表单数据
        x1 = request.form.get('x1')  # 传入表单对应输入字段的 name 值
        x2 = request.form.get('x2')
        # 验证数据
        if not x1 or not x2:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        else:
            try:
                y0 = formula.cal_the_complex_of_1_and_2_generation_of_Ha_0(
                    eval(x1) / 50,
                    eval(x2) / 300)
            except:
                flash('请重新输入，不要输入非数字内容！')  # 显示错误提示
                return redirect(url_for('index'))  # 重定向回主页
        # 保存表单数据到数据库
        global id_user, id_area
        row_ha = Ha_info(
            # id_ha 自增，不必写入
            x1=x1,
            x2=x2,
            y=y0,
            date=date.today(),
            id_user=id_user,  # 需要从 登录用户 获取。这里 global 来的 id_user 已经被登录界面赋值了！
            id_area=
            id_area,  # 需要从 登录用户 获取，参考 test_fk.py。这里 global 来的 id_area 已经被登录界面赋值了！
        )  # 创建记录。
        # row_ha = Ha_info(x1=x1, x2=x2, date=date.today())  # 创建记录
        db.session.add(row_ha)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('写入成功！')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页。与下一行代码只能二选一吗？那线上计算的功能就没了。
        # return render_template('index.html', RESULT=str(y0))# 本意是重定向回主页“return redirect(url_for('index'))”
    # user_info = User_info.query.first()  # 读取农户记录。被删掉是因为有了模板上下文处理函数 inject_user()
    list_ha = Ha_info.query.order_by(db.desc(Ha_info.id_ha)).all(
    )  # 读取所有棉铃虫信息记录，并倒序排列（db.desc(Ha_info.id_ha)）。方便传给前端。
    list_ha_limit = Ha_info.query.order_by(db.desc(
        Ha_info.id_ha)).limit(10).all()  # 读取所有棉铃虫信息记录，但在主页只显示最新的 10 条。
    """<模型类>.query.<过滤方法（可选）>.<查询方法>"""
    return render_template(
        'index.html',
        Area_info=Area_info,
        User_info=User_info,
        list_ha=list_ha,
        list_ha_limit=list_ha_limit,
        RESULT=str(y0),
        RESULT_visitor=str(y00),
        NAME_USER=NAME_USER
    )  # 这里不能用 NAME_USER=current_user.name_user 了，因为“登出”后会报错。


# 编辑 Ha_info 条目
@app.route('/ha_info/edit/<int:id_ha>', methods=['GET', 'POST'])
@login_required  #视图保护
def edit(id_ha):
    row_ha = Ha_info.query.get_or_404(id_ha)

    if request.method == 'POST':  # 处理编辑表单的提交请求
        x1 = request.form['x1']
        x2 = request.form['x2']

        if not x1 or not x2:
            flash('Invalid input.')
            return redirect(url_for('edit', id_ha=id_ha))  # 重定向回对应的编辑页面
        else:
            y0 = formula.cal_the_complex_of_1_and_2_generation_of_Ha_0(
                eval(x1) / 50,
                eval(x2) / 300)
        # 保存更新的表单数据到数据库
        row_ha.x1 = x1  # 更新 x1
        row_ha.x2 = x2  # 更新 x2
        row_ha.y = y0  # 更新 y
        db.session.commit()  # 提交数据库会话
        flash('记录已更新。')
        return redirect(url_for('index'))  # 重定向回主页
        """既然我们要编辑某个条目，那么必然要在输入框里提前把对应的数据放进去，以便于进行更新。在模板里，通过表单 <input> 元素的 value 属性即可将它们提前写到输入框里。"""
    return render_template('edit.html',
                           row_ha=row_ha,
                           NAME_USER=current_user.name_user)  # 传入被编辑的棉铃虫信息记录


# 删除 Ha_info 条目
@app.route('/ha_info/delete/<int:id_ha>', methods=[
    'POST'
])  # 限定只接受 POST 请求。为了安全的考虑，我们一般会使用 POST 请求来提交删除请求，也就是使用表单来实现（而不是创建删除链接）：
@login_required  # 登录保护。添加了这个装饰器后，如果未登录的用户访问对应的 URL，Flask-Login 会把用户重定向到登录页面，并显示一个错误提示。
def delete(id_ha):
    row_ha = Ha_info.query.get_or_404(id_ha)  # 获取电影记录
    db.session.delete(row_ha)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('记录已删除。')
    return redirect(url_for('index'))  # 重定向回主页


# 支持设置、更改用户名字
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name_user = request.form['name_user']
        username = request.form['username']

        if not name_user:
            flash('无效的输入。')
            return redirect(url_for('settings'))
        if User_info.query.filter_by(
                username=username).first() and User_info.query.filter_by(
                    name_user=name_user).first():
            """这里完成判断“是否已被注册”用“and”，登录情况要用“or”。"""
            flash('“称呼”或用户名已被注册，请更改用户名。')  # 如果验证失败，显示错误消息
            return redirect(url_for('settings'))
        current_user.name_user = name_user
        current_user.username = username
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User_info.query.first()
        # user_info.name = name
        db.session.commit()
        flash('您的“称呼”与“用户名”设置成功。')
        return redirect(url_for('index'))

    return render_template('settings.html', NAME_USER=current_user.name_user)


# 对 ha_info 的全面的友好的展示。对 ha_info 进行模糊查询，转向新的视图函数
@app.route('/ha_detail', methods=['GET', 'POST'])
@login_required  # 保护
def ha_detail():
    global list_area_name_area
    if request.method == 'POST':  # 判断是否是 POST 请求
        if not current_user.is_authenticated:  # 如果当前用户未认证
            return redirect(url_for('index'))  # 重定向回主页
        # 认证完毕后获取表单数据
        fuzzy_inquiry_name_area = request.form.get(
            'fuzzy_inquiry_name_area')  # 传入表单对应输入字段的 fuzzy_inquiry_name_area 值
        # 验证数据
        try:
            """返回一个 包含“满足检索要求”的所有记录的 list"""
            list_area = Area_info.query.order_by(db.desc(
                Area_info.id_area)).filter(
                    Area_info.name_area.like(
                        "%{}%".format(fuzzy_inquiry_name_area))).all()
            """用到了python中的正则表达式"""
            list_area_name_area = []  # 使用前需要“清空”
            for row_area in list_area:
                list_area_name_area.append(row_area.name_area)
            """如果“伊”匹配到了“伊犁”和“伊宁”，这都会被传入"""
        except:
            flash('不合规，请重新输入！')  # 显示错误提示
            return redirect(url_for('ha_detail'))  # 重定向回主页
        # 从数据库获取……（获取保存表单数据到数据库）
        flash('查询结果如下：')
        return redirect(
            url_for('ha_detail'))  # 重定向回主页。与下一行代码只能二选一吗？那线上计算的功能就没了。
    list_ha = Ha_info.query.order_by(db.desc(Ha_info.id_ha)).all(
    )  # 读取所有棉铃虫信息记录，并倒序排列（db.desc(Ha_info.id_ha)）。之后传给前端。
    """<模型类>.query.<过滤方法（可选）>.<查询方法>"""
    return render_template(
        'ha_detail.html',
        Area_info=Area_info,
        User_info=User_info,
        list_ha=list_ha,
        list_area_name_area=list_area_name_area,
        NAME_USER=current_user.name_user
    )  # 只有登录后才能进入详细查询页，所以此时 NAME_USER=current_user.name_user 可用


# 对 area_info 的全面的友好的展示。首页点击“管理员……”即可
@app.route('/area_detail', methods=['GET', 'POST'])
@login_required  # 保护
def area_detail():
    global list_area_admin_id_area
    if request.method == 'POST':  # 判断是否是 POST 请求
        if not current_user.is_authenticated:  # 如果当前用户未认证
            return redirect(url_for('index'))  # 重定向回主页
        # 认证完毕后获取表单数据
        fuzzy_inquiry_name_area_admin = request.form.get(
            'fuzzy_inquiry_name_area_admin'
        )  # 传入表单对应输入字段的 fuzzy_inquiry_name_area_admin 值
        # 验证数据
        try:
            """# 返回一个 包含“满足检索要求”的所有记录的 list"""
            list_area_admin = Area_info.query.order_by(
                db.desc(Area_info.id_area)).filter(
                    Area_info.name_area.like(
                        "%{}%".format(fuzzy_inquiry_name_area_admin))).all()
            """用到了python中的正则表达式"""
            list_area_admin_id_area = []  # 使用前需要“清空”
            for row_user_admin in list_area_admin:
                list_area_admin_id_area.append(row_user_admin.id_area)
            """如果“伊”匹配到了“伊犁”和“伊宁”，这都会被传入"""
        except:
            flash('不合规，请重新输入！')  # 显示错误提示
            return redirect(url_for('ha_detail'))  # 重定向回主页
        # 从数据库获取……（获取保存表单数据到数据库）
        flash('查询结果如下：')
        return redirect(url_for('area_detail'))  # 重定向回 area_detail
    # 我之前错了！我想做的是用 user_info 表来引出 area_info 表，而非顺着 admin 就连向 area_info
    list_user = User_info.query.order_by(db.desc(
        User_info.id_area)).all()  # 读取所有地区信息记录，并倒序排列。之后传给前端，表的最左边会用到。
    return render_template('area_detail.html',
                           Area_info=Area_info,
                           User_info=User_info,
                           list_user=list_user,
                           list_area_admin_id_area=list_area_admin_id_area,
                           NAME_USER=current_user.name_user)


# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    global id_user, id_area, NAME_USER
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # name_area = request.form['name_area']  # 这里容易出错！可以不从表单获取，而从外键。注意，记得在 login.html 里更新 <form>
        if not username or not password:
            flash('无效的输入。')
            return redirect(url_for('login'))

        row_user = User_info.query.order_by(db.desc(
            User_info.id_user)).filter_by(username=username).first(
            )  # 其实因为 username 是 UNIQUE，这里用.all()也会只返回一条记录。
        # 验证用户名和密码是否一致
        if row_user:
            """当用户名未写入 User_info，row_user 会查询不到，变成 NoneType，返回 False。这里用 if 来防止报错。 """
            if username == row_user.username and row_user.validate_password(
                    password):
                """在这里改变 global 来的变量"""
                id_user = User_info.query.filter_by(username=username).first(
                ).id_user  # 就在这外键连接，用 filter_by()。这样就可以在 '/' 下把 id_user 的值赋给 row_ha 中的 id_user 了。

                id_area = User_info.query.filter_by(username=username).first(
                ).id_area  # 就在这外键连接，用 filter_by()。这样就可以在 '/' 下把 id_area 的值赋给 row_ha 中的 id_area 了。
                NAME_USER = User_info.query.filter_by(
                    username=username).first().name_user

                login_user(row_user)  # 登入用户。注意这里要选用特定的 column
                flash('登录成功')
                return redirect(url_for('index'))  # 重定向到主页
            else:
                flash('您的用户名与密码不匹配。')  # 如果验证失败，显示错误消息
                return redirect(url_for('login'))  # 重定向回登录页面
        else:
            flash('您的用户名未注册，现帮您跳至注册页')  # 如果验证失败，显示错误消息
            return redirect(url_for('register'))  # 重定向回注册
    else:
        return render_template('login.html')


# 用户注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        """填入注册必需的信息"""
        name_user = request.form['name_user']
        username = request.form['username']
        password_hash = request.form['password']
        name_area = request.form['name_area']  # 这里会想办法用外键连接实现的

        if not name_user or not username or not password_hash:
            """不允许什么都不输入"""
            flash('无效的输入。')
            return redirect(url_for('register'))  # 重定向回注册页面
        else:
            """验证是否被注册"""
            if User_info.query.filter_by(
                    username=username).first() or User_info.query.filter_by(
                        name_user=name_user).first():
                """从 user_info 表的 username"""
                flash('“称呼”或用户名已被注册，请更改用户名。')  # 如果验证失败，显示错误消息
                return redirect(url_for('register'))

            # 信息写入 Area_info
            else:
                row_area = Area_info(name_area=name_area)
            if Area_info.query.filter_by(name_area=name_area).first():
                flash('这个地区不止您一位注册')  # 如果验证失败，显示错误消息
                db.session.commit(
                )  # 先把 name_area 提交数据库的 area_info 表中，这将自动生成 id_area。管理员的 id_admin 先不管了。
            else:
                flash('在这个地区，您是第一位注册')
                db.session.add(row_area)  # 添加到数据库会话
                db.session.commit(
                )  # 先把 name_area 提交数据库的 area_info 表中，这将自动生成 id_area。管理员的 id_admin 先不管了。

            # 信息写入 User_info
            row_user = User_info(
                name_user=name_user,
                username=username,
                password_hash=generate_password_hash(password_hash),
                id_area=Area_info.query.filter_by(name_area=name_area).first().
                id_area  # 这里用外键，filter_by()。借助先前把 name_area提交数据库的 area_info 表中自动生成的 id_area。
            )
            db.session.add(row_user)  # 添加到数据库会话
            db.session.commit()  # 提交数据库会话
            flash('注册成功。已跳转至登录页，请登录')  # 如果验证失败，显示错误消息
            return redirect(url_for('login'))
    else:
        return render_template('register.html')


# 与登录相对，登出操作则需要调用 logout_user() 函数，使用下面的视图函数实现
@app.route('/logout')
@login_required  # 用于视图保护，后面会详细介绍
def logout():
    global y0, y00, id_user, id_area, NAME_USER, list_area_name_area, list_area_admin_id_area  # VSC 绝了，可以知道这一行 global 来的变量在哪被“修改过！！！”
    """初始化"""
    y0 = ''
    y00 = ''
    id_user = ''
    id_area = ''
    NAME_USER = ''
    list_area_name_area = []  # 虽然说每次查询前都要清空，但……这里会不会出现“头咬尾巴”的情况啊
    list_area_admin_id_area = []
    logout_user()  # 登出用户
    flash('再见~')
    return redirect(url_for('index'))  # 重定向回首页
