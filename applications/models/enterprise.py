from decimal import Decimal

from applications.extensions import db


class Enterprise(db.Model):
    __tablename__='enterprise'
    enterpriseId=db.Column(db.Integer, primary_key=True, autoincrement=True, comment='商家编号')
    enterpriseName=db.Column(db.String(50), comment='商家名字')
    address=db.Column(db.String(50), comment='商家地址')
    telephone=db.Column(db.String(11), comment='商家联系电话')
    score=db.Column(db.Numeric(precision=2, scale=1), default=Decimal('0.0'), comment='商家评分')
    parentId=db.Column(db.Integer,comment='父类Id')
