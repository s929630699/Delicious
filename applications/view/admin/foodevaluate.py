from flask import Blueprint, render_template, request, jsonify

from applications.common import curd
from applications.common.utils.http import fail_api, success_api, table_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import Foodevaluate, User, Food
from applications.schemas import FoodevaluateOutSchema

foodevaluate = Blueprint('foodevaluate',__name__,url_prefix='/admin/foodevaluate')

@foodevaluate.get('/')
@authorize('admin:foodevaluate:main')
def main():
    return render_template('admin/foodevaluate/main.html')

@foodevaluate.get('/data')
@authorize("admin:foodevaluate:main", log=True)
def data():
    realname = str_escape(request.args.get('realname', type=str))
    foodName = str_escape(request.args.get('foodName', type=str))
    filters = []
    if realname:
        filters.append(User.realname.contains(realname))
    if foodName:
        filters.append(Food.foodName.contains(foodName))
    foodevaluate_data=db.session.query(Foodevaluate,User,Food).join(User,Foodevaluate.userId==User.id).join(Food,Foodevaluate.foodId==Food.foodId).filter(*filters).layui_paginate()
    print(foodevaluate_data)
    return table_api(
        data=[{
            'evaluateId': foodevaluate.evaluateId,
            'userId': foodevaluate.userId,
            'realname':user.realname if user else None,
            'foodId': foodevaluate.foodId,
            'foodName':food.foodName if food else None,
            'score': foodevaluate.score,
            'content': foodevaluate.content,
            'setupTime': foodevaluate.setupTime
        } for foodevaluate, user,food in foodevaluate_data.items],
        count=foodevaluate_data.total)

@foodevaluate.get('/edit/<int:evaluateId>')
@authorize("admin:foodevaluate:edit", log=True)
def edit(evaluateId):
    foodevaluate = Foodevaluate.query.filter_by(evaluateId=evaluateId).first()
    realname=User.query.filter_by(id=foodevaluate.userId).first().realname
    foodName=Food.query.filter_by(foodId=foodevaluate.foodId).first().foodName
    return render_template('admin/foodevaluate/edit.html', foodevaluate=foodevaluate,realname=realname,foodName=foodName)

@foodevaluate.put('/update')
@authorize("admin:foodevaluate:edit", log=True)
def update():
    json = request.get_json(force=True)
    evaluateId = json.get("evaluateId"),
    data = {
        "score": str_escape(json.get("score")),
        "content": str_escape(json.get("content")),
    }
    d = Foodevaluate.query.filter_by(evaluateId=evaluateId).update(data)
    if not d:
        return fail_api(msg="更新失败")
    db.session.commit()
    return success_api(msg="更新成功")

@foodevaluate.delete('/remove/<int:evaluateId>')
@authorize("admin:foodevaluate:remove", log=True)
def remove(evaluateId):
    f = Foodevaluate.query.filter_by(evaluateId=evaluateId).delete()
    if not f:
        return fail_api(msg="删除失败")
    db.session.commit()
    return success_api(msg="删除成功")

# 批量删除
@foodevaluate.delete('/batchRemove')
@authorize("admin:foodevaluate:remove", log=True)
def batch_remove():
    ids = request.form.getlist('ids[]')
    print(ids)
    for evaluateId in ids:
        r = Foodevaluate.query.filter_by(evaluateId=evaluateId).delete()
        if not r:
            return fail_api(msg="删除失败")
        db.session.commit()
    return success_api(msg="批量删除成功")