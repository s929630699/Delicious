import os
from datetime import datetime

from flask import Blueprint, render_template, request, jsonify, current_app
from sqlalchemy import desc

from applications.common import curd
from applications.common.curd import get_one_by_foodId
from applications.common.utils.http import table_api, success_api, fail_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.extensions.init_upload import photos
from applications.models import Food, Foodtype, Enterprise
from applications.common.utils import upload as upload_curd

food = Blueprint('food',__name__,url_prefix='/admin/food')

@food.get('/')
@authorize('admin:food:main')
def main():
    return render_template('admin/food/main.html')

@food.get('/data')
@authorize('admin:food:main')
def date():
    foodName=str_escape(request.args.get('foodName', type=str))
    foodType = str_escape(request.args.get('foodType', type=int))
    enterpriseId=str_escape(request.args.get('enterpriseId', type=int))
    filters = []
    if foodName:
        filters.append(Food.foodName.contains(foodName))
    if foodType:
        filters.append(Food.foodType.contains(foodType))
    if enterpriseId:
        filters.append(Food.enterpriseId.contains(enterpriseId))
    foods = db.session.query(Food,Foodtype,Enterprise).join(Foodtype,Food.foodType==Foodtype.foodTypeId).join(Enterprise,Food.enterpriseId==Enterprise.enterpriseId).filter(*filters).layui_paginate()
    return table_api(
        data=[{
            'foodId':food.foodId,
            'foodName':food.foodName,
            'foodImage':food.foodImage,
            'foodType':food.foodType,
            'foodTypeName':foodtype.foodTypeName,
            'price':food.price,
            'launchDate':food.launchDate,
            'saleCount':food.saleCount,
            'hits':food.hits,
            'collectQuantity':food.collectQuantity,
            'introduce':food.introduce,
            'enterpriseId':food.enterpriseId,
            'enterpriseName':enterprise.enterpriseName
        } for food,foodtype,enterprise in foods]
        , count=foods.total)





@food.get('/add')
@authorize("admin:food:add", log=True)
def add():
    return render_template('admin/food/add.html')

@food.post('/save')
@authorize("admin:food:add", log=True)
def save():
    req = request.get_json(force=True)
    foodName=str_escape(req.get("foodName"))
    file=str_escape(req.get("file"))
    foodImage='/_uploads/photos/'+file[file.rfind('\\')+1:]
    foodType = str_escape(req.get("foodType"))
    price = str_escape(req.get("price"))
    launchDate = datetime.now()
    saleCount=0
    hits=0
    collectQuantity=0
    introduce= str_escape(req.get("introduce"))
    enterpriseId = str_escape(req.get("enterpriseId"))

    food = Food(
        foodName=foodName,
        foodImage=foodImage,
        foodType=foodType,
        price=price,
        launchDate=launchDate,
        saleCount=saleCount,
        hits = hits,
        collectQuantity = collectQuantity,
        introduce=introduce,
        enterpriseId=enterpriseId
    )
    db.session.add(food)
    db.session.commit()
    return success_api(msg="添加成功")

#   上传接口
@food.post('/upload')
@authorize("admin:food:add", log=True)
def upload_api():
    if 'file' in request.files:
        photo = request.files['file']
        mime = request.files['file'].content_type

        food=Food.query.order_by(desc(Food.foodId)).first()
        file_url = upload_curd.upload_one(photo=photo)
        res = {
            "msg": "上传成功",
            "code": 0,
            "success": True,
            "data":
                {"src": file_url}
        }
        return jsonify(res)
    return fail_api()

# 美食套餐编辑
@food.get('/edit/<int:foodId>')
@authorize("admin:food:edit", log=True)
def edit(foodId):
    food = get_one_by_foodId(model=Food, foodId=foodId)
    return render_template('admin/food/edit.html', food=food)


# 更新美食套餐
@food.put('/update')
@authorize("admin:food:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    foodId = req_json.get("foodId")
    file = str_escape(req_json.get("file"))
    foodImage = '/_uploads/photos/' + file[file.rfind('\\') + 1:]
    data = {
        "foodName" :str_escape(req_json.get("foodName")),
        "foodImage" :foodImage,
        "foodType" :str_escape(req_json.get("foodType")),
        "price" :str_escape(req_json.get("price")),
        "introduce" :str_escape(req_json.get("introduce")),
        "enterpriseId" :str_escape(req_json.get("enterpriseId")),
    }
    food = Food.query.filter_by(foodId=foodId).update(data)
    db.session.commit()
    if not food:
        return fail_api(msg="更新失败")
    return success_api(msg="更新成功")

# 删除
@food.delete('/remove/<int:foodId>')
@authorize("admin:food:remove", log=True)
def remove(foodId):
    r = Food.query.filter_by(foodId=foodId).delete()
    db.session.commit()
    if not r:
        return fail_api(msg="删除失败")
    return success_api(msg="删除成功")


# 批量删除
@food.delete('/batchRemove')
@authorize("admin:food:remove", log=True)
def batch_remove():
    ids = request.form.getlist('ids[]')
    print(ids)
    for foodId in ids:
        r = Food.query.filter_by(foodId=foodId).delete()
        db.session.commit()
    return success_api(msg="批量删除成功")