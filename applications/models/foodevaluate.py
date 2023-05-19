from decimal import Decimal

from applications.extensions import db


class Foodevaluate(db.Model):
    __tablename__='foodevaluate'
    evaluateId=db.Column(db.Integer, primary_key=True, autoincrement=True, comment='点评编号')
    userId=db.Column(db.Integer, comment='用户编号')
    foodId=db.Column(db.Integer, comment='美食编号')
    score = db.Column(db.Numeric(precision=2, scale=1), default=Decimal('0.0'), comment='评分')
    content = db.Column(db.Text, comment='内容')
    setupTime = db.Column(db.DateTime, comment='发布日期')