from myha import db  # 导入模型类、db变量
from myha.models import Area_info, User_info

list_area_admin = Area_info.query.order_by(db.desc(Area_info.id_area)).filter(
    Area_info.name_area.like("%{}%".format('伊'))).all()

print(list_area_admin)

list_area_admin_id_area = []  # 使用前需要“清空”
for row_user_admin in list_area_admin:
    list_area_admin_id_area.append(row_user_admin.id_area)

print(list_area_admin_id_area)

# 我之前错了！我想做的是用 user_info 表来引出 area_info 表，而非顺着 admin 就连向 area_info
list_user = User_info.query.order_by(db.desc(
    User_info.id_area)).all()  # 读取所有地区信息记录，并倒序排列。之后传给前端，表的最左边会用到。

print(list_user)
i = 1
for row_user in list_user:
    if  User_info.query.filter_by(id_area=row_user.id_area).first().id_area in  list_area_admin_id_area:
        print(row_user.id_area, end="\t")
        print(Area_info.query.filter_by(id_area=row_user.id_area).first().name_area, end="\t")
        print(row_user.id_user, end="\t")
        print(row_user.name_user, end="\t")
        print(row_user.username, end="\t")
        print(row_user.id_area, end="\t")
        i += 1
        print("\n")
