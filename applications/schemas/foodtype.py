from applications.extensions import ma
from marshmallow import fields


class FoodtypeOutSchema(ma.Schema):
    foodTypeId = fields.Integer()
    foodTypeName = fields.Str()
    memo = fields.Str()
    parentId=fields.Integer()
