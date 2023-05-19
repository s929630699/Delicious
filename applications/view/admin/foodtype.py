from flask import Blueprint, render_template, jsonify, request

from applications.common import curd
from applications.common.utils.http import success_api, fail_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import Foodtype, Food
from applications.schemas import FoodtypeOutSchema

foodtype = Blueprint('foodtype',__name__,url_prefix='/admin/foodtype')

@foodtype.get('/')
@authorize('admin:foodtype:main')
def main():
    return render_template('admin/foodtype/main.html')

@foodtype.post('/data')
@authorize("admin:foodtype:main", log=True)
def data():
    foodtype = Foodtype.query.order_by(Foodtype.parentId).all()
    foodtype_data = curd.model_to_dicts(schema=FoodtypeOutSchema, data=foodtype)
    res = {
        "data": foodtype_data
    }
    return jsonify(res)

@foodtype.get('/selectFoodType')
@authorize('admin:food:main',log=True)
def selectFoodType():
    foodtype=Foodtype.query.all()
    res = curd.model_to_dicts(schema=FoodtypeOutSchema, data=foodtype)
    res = {
        "status": {"code": 200, "message": "默认"},
        "data": res
    }
    return jsonify(res)

@foodtype.get('/selectParent')
@authorize("admin:foodtype:main", log=True)
def select_parent():
    foodtype = Foodtype.query.all()
    res = curd.model_to_dicts(schema=FoodtypeOutSchema, data=foodtype)
    res.append({"foodTypeId": 0, "foodTypeName": "一级分类", "parentId": -1})
    res = {
        "status": {"code": 200, "message": "默认"},
        "data": res
    }
    return jsonify(res)

@foodtype.get('/add')
@authorize("admin:foodtype:add", log=True)
def add():
    return render_template('admin/foodtype/add.html')


@foodtype.post('/save')
@authorize("admin:foodtype:add", log=True)
def save():
    req_json = request.get_json(force=True)
    foodtype = Foodtype(
        foodTypeName=str_escape(req_json.get('foodTypeName')),
        memo=str_escape(req_json.get('memo')),
        parentId=str_escape(req_json.get('parentId')),
    )
    db.session.add(foodtype)
    db.session.commit()
    return success_api(msg="添加成功")

@foodtype.get('/edit')
@authorize("admin:foodtype:edit", log=True)
def edit():
    foodTypeId = request.args.get("foodTypeId")
    foodtype = curd.get_one_by_foodTypeId(model=Foodtype, foodTypeId=foodTypeId)
    return render_template('admin/foodtype/edit.html', foodtype=foodtype)

@foodtype.put('/update')
@authorize("admin:foodtype:edit", log=True)
def update():
    json = request.get_json(force=True)
    foodTypeId = json.get("foodTypeId"),
    data = {
        "foodTypeName": str_escape(json.get("foodTypeName")),
        "memo": str_escape(json.get("memo")),
        "parentId": str_escape(json.get("parentId"))
    }
    d = Foodtype.query.filter_by(foodTypeId=foodTypeId).update(data)
    if not d:
        return fail_api(msg="更新失败")
    db.session.commit()
    return success_api(msg="更新成功")

@foodtype.delete('/remove/<int:foodTypeId>')
@authorize("admin:foodtype:remove", log=True)
def remove(foodTypeId):

    if Food.query.filter_by(foodType=foodTypeId).all() !=[]:
        res = Food.query.filter_by(foodType=foodTypeId).update({"foodType": None})
        if not res:
            return fail_api(msg="删除失败")

    f = Foodtype.query.filter_by(foodTypeId=foodTypeId).delete()
    if not f:
        return fail_api(msg="删除失败")
    db.session.commit()
    return success_api(msg="删除成功")

# 批量删除
@foodtype.delete('/batchRemove')
@authorize("admin:foodtype:remove", log=True)
def batch_remove():
    ids = request.form.getlist('ids[]')
    print(ids)
    for foodTypeId in ids:
        if Foodtype.query.filter_by(parentId=foodTypeId).first() is None:
            continue
        elif Foodtype.query.filter_by(parentId=foodTypeId).first().parentId in ids:
            continue
        if Food.query.filter_by(foodType=foodTypeId).all() != []:
            res = Food.query.filter_by(foodType=foodTypeId).update({"foodType": None})
            if not res:
                return fail_api(msg="删除失败")
        r = Foodtype.query.filter_by(foodTypeId=foodTypeId).delete()
        s = Foodtype.query.filter_by(parentId=foodTypeId).delete()
        if not r and not s:
            return fail_api(msg="删除失败")
        db.session.commit()
    return success_api(msg="批量删除成功")

