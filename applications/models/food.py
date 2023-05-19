from decimal import Decimal

from applications.extensions import db


class Food(db.Model):
    __tablename__='food'
    foodId=db.Column(db.Integer, primary_key=True, autoincrement=True, comment='美食id')
    foodName=db.Column(db.String(50), comment='美食名称')
    foodImage=db.Column(db.String(50), comment='美食海报')
    foodType = db.Column(db.Integer, comment='美食类型')
    price = db.Column(db.Numeric(precision=10, scale=2), default=Decimal('0.00'), comment='价格')
    launchDate = db.Column(db.DateTime, comment='上架日期')
    saleCount = db.Column(db.Integer, comment='销售数量')
    hits = db.Column(db.Integer, comment='点击数')
    collectQuantity = db.Column(db.Integer, comment='收藏量')
    introduce = db.Column(db.Text, comment='美食介绍')
    enterpriseId = db.Column(db.String(50), comment='所属商家')
