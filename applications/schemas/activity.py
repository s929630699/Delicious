from applications.extensions import ma
from marshmallow import fields


class ActivityOutSchema(ma.Schema):
    activityId = fields.Integer()
    title = fields.Str()
    image = fields.Str()
    contents=fields.Str()
    addtime=fields.DateTime()
    hits=fields.Integer()
