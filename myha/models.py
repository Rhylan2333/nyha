# -*- coding: utf-8 -*-
# 模型类

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from myha import db


# 管理员 表
class Admin_info(db.Model, UserMixin):  # 表名将会是 user_info （自动生成，小写处理）
    id_admin = db.Column(db.Integer, primary_key=True)  # 主键，管理员id
    name_admin = db.Column(db.String(20), unique=True)  # 管理员称呼
    list_area_info = db.relationship(
        'Area_info',
        backref='area')  # 这里新建了一个名叫 area 的属性用来表示当前模型中包含的 Area_info 列表。
    """
    第一部分 —— 'Area_info' 表示关系另一端的模型的名称。
    第二部分 —— 是一个名叫 backref 的参数，叫做反向关系，我们将其设置成 'area_info' ，
        它会向 Area_info 模型中添加一个名叫 area_info 的属性，
        这个属性可以替代 id_admin（FK） 访问 Area_info 模型，但是它获取的是 Area_info 模型的对象，而非 Area_info 模型中 id_admin（FK）对应的值。
    """
    adminname = db.Column(db.String(20))  #管理员的用户名
    password_hash = db.Column(db.String(128))  # 管理员的密码

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值

    def get_id(self):
        """添加一个get_id()函数，以便覆盖由 models.py 定义的数据库架构的文件"""
        """"表示感谢https://www.cnpython.com/qa/162793"""
        return (self.id_admin)


# 地区 表
class Area_info(db.Model):  # 表名将会是 area_info （自动生成，小写处理）
    id_area = db.Column(db.Integer, primary_key=True)  # 主键，地区id
    name_area = db.Column(db.String(20), unique=True)  # 地区名
    list_ha_info = db.relationship('Ha_info', backref='ha')
    list_user_info = db.relationship('User_info', backref='user')
    id_admin = db.Column(db.Integer,
                         db.ForeignKey('admin_info.id_admin'))  # 外键，管理员id


# 农户 表
class User_info(db.Model, UserMixin):  # 表名将会是 user_info （自动生成，小写处理）
    """
    在存储用户信息的 User 模型类添加 username 字段和 password_hash 字段，分别用来存储登录所需的用户名和密码散列值，同时添加两个方法来实现设置密码和验证密码的功能：
    
    Flask-Login 提供了一个 current_user 变量，注册这个函数的目的是，当程序运行后，如果用户已登录， current_user 变量的值会是当前用户的用户模型类记录。另一个步骤是让存储用户的 User 模型类继承 Flask-Login 提供的 UserMixin 类：
    继承 UserMixin 这个类会让 User_info 类拥有几个用于判断认证状态的属性和方法，
        其中最常用的是 is_authenticated 属性：如果当前用户已经登录，那么 current_user.is_authenticated 会返回 True， 否则返回 False。
    有了 current_user 变量和这几个验证方法和属性，我们可以很轻松的判断当前用户的认证状态。
    """
    id_user = db.Column(db.Integer, primary_key=True)  # 主键，农户id
    name_user = db.Column(db.String(20), unique=True)  # 农户称呼
    list_ha_info = db.relationship('Ha_info', backref='ha_info')  # 这个功能未能实现
    username = db.Column(db.String(20), unique=True)  # 农户的用户名
    password_hash = db.Column(db.String(128))  # 农户密码
    id_area = db.Column(db.Integer,
                        db.ForeignKey('area_info.id_area'))  # 外键，农户所属地区id

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值

    def get_id(self):
        """"表示感谢https://www.cnpython.com/qa/162793"""
        return (self.id_user)


# 棉铃虫信息 表
class Ha_info(db.Model):  # 表名将会是 ha_info
    id_ha = db.Column(db.Integer, primary_key=True)  # 主键
    x1 = db.Column(db.Float)  # 一代幼虫量(头／百株)
    x2 = db.Column(db.Float)  # 二代幼虫量(头／百株)
    y = db.Column(db.Float)  # 理论产量损失率(%)
    date = db.Column(db.Date, default=date.today())  # 记录时间
    id_user = db.Column(db.Integer,
                        db.ForeignKey('user_info.id_user'))  # 外键，记录农户id
    id_area = db.Column(db.Integer,
                        db.ForeignKey('area_info.id_area'))  # 外键，记录地区id
