from applications.extensions import db

# # 创建中间表
# user_role = db.Table(
#     __tablename__="admin_user_role",  # 中间表名称
#     id=db.Column("id", db.Integer, primary_key=True, autoincrement=True, comment='标识'),  # 主键
#     user_id=db.Column("user_id", db.Integer, db.ForeignKey("admin_user.id"), comment='用户编号'),  # 属性 外键
#     role_id=db.Column("role_id", db.Integer, db.ForeignKey("admin_role.id"), comment='角色编号'),  # 属性 外键
# )

class user_role(db.Model):
    __tablename__="admin_user_role"  # 中间表名称
    id=db.Column("id", db.Integer, primary_key=True, autoincrement=True, comment='标识')  # 主键
    user_id=db.Column("user_id", db.Integer, db.ForeignKey("admin_user.id"), comment='用户编号')  # 属性 外键
    role_id=db.Column("role_id", db.Integer, db.ForeignKey("admin_role.id"), comment='角色编号')  # 属性 外键
