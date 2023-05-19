from applications.extensions import db


class Foodtype(db.Model):
    __tablename__='foodType'
    foodTypeId=db.Column(db.Integer, primary_key=True, autoincrement=True, comment='美食类型id')
    foodTypeName=db.Column(db.String(40), comment='美食类型名称')
    memo=db.Column(db.Text, comment='备注')
    parentId=db.Column(db.Integer,comment='父类Id')
