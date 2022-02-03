# 命令函数# -*- coding: utf-8 -*-
from datetime import date

import click
from werkzeug.security import check_password_hash, generate_password_hash

from myha import app, db
from myha.models import Admin_info, Area_info, Ha_info, User_info


@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """默认情况下，函数名称就是命令的名字，现在执行 flask initdb 命令就可以创建数据库表："""
    """使用 --drop 选项可以删除表后重新创建"""
    if drop:  # 判断是否输入了选项”
        """如果输入命令“initdb --drop”"""
        db.drop_all()
        print("数据库已清空。")
    db.create_all()
    click.echo('数据库已初始化。')  # 输出提示信息


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    list_admin = [{
        'id_admin': 0,
        'name_admin': '管理员0',
        'adminname': 'guanliyua',
        'password_hash': generate_password_hash('123456')
    }]  # 创建 admin 实例

    list_area = [{
        'id_area': 0,
        'name_area': "伊犁",
        'id_admin': 0  # 这是外键
    }]  # 创建 area 实例

    list_user = [{
        'id_user': 0,
        'name_user': '农户0',
        'username': 'nonghu',
        'password_hash': generate_password_hash('123'),
        'id_area': 0  # 这是外键
    }]  # 创建 user 实例

    list_ha = [{
        'id_ha': 5,
        'x1': 50,
        'x2': 300,
        'y': '25.624243',
        'date': date(2022, 1, 29),
        'id_user': 5,
        'id_area': 5
    }, {
        'id_ha': 1,
        'x1': 10,
        'x2': 60,
        'y': 15.435247,
        'date': date(2022, 1, 25),
        'id_user': 1,
        'id_area': 1
    }, {
        'id_ha': 2,
        'x1': 20,
        'x2': 120,
        'y': 17.6739028,
        'date': date(2022, 1, 26),
        'id_user': 2,
        'id_area': 2
    }, {
        'id_ha': 3,
        'x1': 30,
        'x2': 180,
        'y': 20.1182874,
        'date': date(2022, 1, 27),
        'id_user': 3,
        'id_area': 3
    }, {
        'id_ha': 4,
        'x1': 40,
        'x2': 250,
        'y': 22.768400800000002,
        'date': date(2022, 1, 28),
        'id_user': 4,
        'id_area': 4
    }]

    for row_admin in list_admin:
        """在此实现下两行 admin 实例所对应的 Admin_info 模型中定义的 list_area_info 接着由 relationship 生成的 InstrumentedList"""
        # print(row_admin)
        admin = Admin_info(
            id_admin=row_admin['id_admin'],
            name_admin=row_admin['name_admin'],
            adminname=row_admin['adminname'],
            password_hash=row_admin['password_hash']
        )  # 把这个 def 中的 name_admin = 'Yuhao Cai' 左传给 Admin_info 模型中的 name_admin
        # print(admin)  # 检查此实例是否创建成功
        db.session.add(admin)

    for row_area in list_area:
        # print(row_area)
        area = Area_info(
            id_area=row_area['id_area'],
            name_area=row_area['name_area'],
            id_admin=row_area['id_admin']  # 这是外键
        )  # 创建实例
        # print(area)  # 检查此实例是否创建成功

        admin.list_area_info.append(
            area)  # 向 admin 实例中的 relationship 生成的 list_area_info 传入 area 实例
        # print(admin.list_area_info[-1].name_area)  # 获取 InstrumentedList 的倒数第一个元素

        db.session.add(area)

    for row_user in list_user:
        # print(row_user)
        user = User_info(
            id_user=row_user['id_user'],
            name_user=row_user['name_user'],
            username=row_user['username'],
            password_hash=row_user['password_hash'],
            id_area=row_user['id_area']
        )  # 把这个 def 中的 name_user = '蔡雨豪' 左传给 User_info 模型中的 name_user
        # print(user)

        area.list_user_info.append(
            user)  # 向 area 实例中的 relationship 生成的 list_user_info 传入 user 实例
        # print(area.list_user_info[-1].name_user)  # 获取 InstrumentedList 的倒数第一个元素

        db.session.add(user)

    for row_ha in list_ha:
        print(row_ha)
        ha = Ha_info(
            id_ha=row_ha['id_ha'],
            x1=row_ha['x1'],
            x2=row_ha['x2'],
            y=row_ha['y'],
            date=row_ha['date'],
            id_user=row_ha['id_user'],
            id_area=row_ha['id_area']
        )  # 创建一个 row_ha 记录，等号左边的“x1、x2、y”与ha_info表中的“x1、x2、y”要匹配/相等
        # print(ha)

        area.list_ha_info.append(
            ha
        )  # 向 area 实例中的 relationship 生成的 list_ha_info 传入 ha 实例。源自 print(area.list_ha_info)
        user.list_ha_info.append(
            ha
        )  # 向 user 实例中的 relationship 生成的 list_ha_info 传入 ha 实例。源自 print(user.list_ha_info)
        # print(area.list_ha_info[-1].id_user)  # 获取 InstrumentedList 的倒数第一个元素
        # print(user.list_ha_info[-1].id_area)  # 获取 InstrumentedList 的倒数第一个元素

        db.session.add(ha)

    db.session.commit()
    db.session.close()
    click.echo('虚拟数据已写入数据库 my_ha_data。')


# 生成农户账户
@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password',
              prompt=True,
              hide_input=True,
              confirmation_prompt=True,
              help='The password used to login.'
              )  # 使用 click.option() 装饰器设置的两个选项分别用来接受输入用户名和密码。
def user(username, password):
    """创建农户 user"""
    db.create_all()

    user = User_info.query.first()
    if user is not None:
        click.echo('Updating `农户` user...')
        user.username = username
        user.set_password(password)  # 设置密码
    else:
        click.echo('Creating `农户` user...')
        user = User_info(username=username, name_user='0号 user')
        user.set_password(password)  # 设置密码
        db.session.add(user)

    db.session.commit()  # 提交数据库会话
    click.echo('User Created!')


# 生成管理员账户
@app.cli.command()
@click.option('--adminname', prompt=True, help='The adminrname used to login.')
@click.option('--password',
              prompt=True,
              hide_input=True,
              confirmation_prompt=True,
              help='The password used to login.'
              )  # 使用 click.option() 装饰器设置的两个选项分别用来接受输入用户名和密码。
def admin(adminname, password):
    """创建管理员 admin"""
    db.create_all()

    admin = Admin_info.query.first()
    if admin is not None:
        click.echo('Updating `管理员` admin...')
        admin.adminname = adminname
        admin.set_password(password)  # 设置密码
    else:
        click.echo('Creating `管理员` admin...')
        admin = Admin_info(adminname=adminname, name_admin='0号 admin')
        admin.set_password(password)  # 设置密码
        db.session.add(admin)

    db.session.commit()  # 提交数据库会话
    click.echo('Admin Created!')
