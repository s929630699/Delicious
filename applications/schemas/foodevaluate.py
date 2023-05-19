from applications.extensions import ma
from marshmallow import fields


class FoodevaluateOutSchema(ma.Schema):
    evaluateId = fields.Integer()
    userId = fields.Integer()
    foodId = fields.Integer()
    score=fields.Decimal()
    content=fields.Str()
    setupTime=fields.DateTime()
