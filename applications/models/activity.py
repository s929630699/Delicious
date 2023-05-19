from decimal import Decimal

from applications.extensions import db


class Activity(db.Model):
    __tablename__='activity'
    activityId=db.Column(db.Integer, primary_key=True, autoincrement=True, comment='活动编号')
    title=db.Column(db.String(40), comment='标题')
    image=db.Column(db.String(150), comment='图片')
    contents = db.Column(db.Text, comment='内容')
    addtime = db.Column(db.DateTime, comment='发布日期')
    hits = db.Column(db.Integer, comment='点击量')
