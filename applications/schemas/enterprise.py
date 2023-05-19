from applications.extensions import ma
from marshmallow import fields


class EnterpriseOutSchema(ma.Schema):
    enterpriseId = fields.Integer()
    enterpriseName = fields.Str()
    address = fields.Str()
    telephone = fields.Str()
    score = fields.Decimal()
    parentId=fields.Integer()
