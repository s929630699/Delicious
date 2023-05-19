from flask import Blueprint, render_template, jsonify, request

from applications.common import curd
from applications.common.utils.http import success_api, fail_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import Enterprise, Food
from applications.schemas import EnterpriseOutSchema

enterprise = Blueprint('enterprise',__name__,url_prefix='/admin/enterprise')

@enterprise.get('/')
@authorize('admin:enterprise:main')
def main():
    return render_template('admin/enterprise/main.html')

@enterprise.post('/data')
@authorize("admin:enterprise:main", log=True)
def data():
    enterprise = Enterprise.query.order_by(Enterprise.parentId).all()
    enterprise_data = curd.model_to_dicts(schema=EnterpriseOutSchema, data=enterprise)
    res = {
        "data": enterprise_data
    }
    return jsonify(res)

@enterprise.get('/selectEnterprise')
@authorize('admin:food:main',log=True)
def selectEnterprise():
    enterprise=Enterprise.query.all()
    res = curd.model_to_dicts(schema=EnterpriseOutSchema, data=enterprise)
    res = {
        "status": {"code": 200, "message": "默认"},
        "data": res
    }
    return jsonify(res)

@enterprise.get('/selectParent')
@authorize("admin:enterprise:main", log=True)
def select_parent():
    enterprise = Enterprise.query.all()
    res = curd.model_to_dicts(schema=EnterpriseOutSchema, data=enterprise)
    res.append({"enterpriseId": 0, "enterpriseName": "一级分类", "parentId": -1})
    res = {
        "status": {"code": 200, "message": "默认"},
        "data": res
    }
    return jsonify(res)

@enterprise.get('/add')
@authorize("admin:enterprise:add", log=True)
def add():
    return render_template('admin/enterprise/add.html')


@enterprise.post('/save')
@authorize("admin:enterprise:add", log=True)
def save():
    req_json = request.get_json(force=True)
    enterprise = Enterprise(
        enterpriseName=str_escape(req_json.get('enterpriseName')),
        address=str_escape(req_json.get('address')),
        telephone=str_escape(req_json.get('telephone')),
        score=str_escape(req_json.get('score')),
        parentId=str_escape(req_json.get('parentId')),
    )
    db.session.add(enterprise)
    db.session.commit()
    return success_api(msg="添加成功")

@enterprise.get('/edit')
@authorize("admin:enterprise:edit", log=True)
def edit():
    enterpriseId = request.args.get("enterpriseId")
    enterprise = Enterprise.query.filter_by(enterpriseId=enterpriseId).first()
    return render_template('admin/enterprise/edit.html', enterprise=enterprise)

@enterprise.put('/update')
@authorize("admin:enterprise:edit", log=True)
def update():
    json = request.get_json(force=True)
    enterpriseId = json.get("enterpriseId"),
    data = {
        "enterpriseName": str_escape(json.get("enterpriseName")),
        "address": str_escape(json.get("address")),
        "telephone": str_escape(json.get("telephone")),
        "score": str_escape(json.get("score")),
        "parentId": str_escape(json.get("parentId"))
    }
    d = Enterprise.query.filter_by(enterpriseId=enterpriseId).update(data)
    if not d:
        return fail_api(msg="更新失败")
    db.session.commit()
    return success_api(msg="更新成功")

@enterprise.delete('/remove/<int:enterpriseId>')
@authorize("admin:enterprise:remove", log=True)
def remove(enterpriseId):
    if Food.query.filter_by(enterpriseId=enterpriseId).all() !=[]:
        res = Food.query.filter_by(enterpriseId=enterpriseId).update({"enterpriseId": None})
        if not res:
            return fail_api(msg="删除失败")

    f = Enterprise.query.filter_by(enterpriseId=enterpriseId).delete()
    if not f:
        return fail_api(msg="删除失败")
    db.session.commit()
    return success_api(msg="删除成功")

# 批量删除
@enterprise.delete('/batchRemove')
@authorize("admin:enterprise:remove", log=True)
def batch_remove():
    ids = request.form.getlist('ids[]')
    print(ids)
    for enterpriseId in ids:
        if Enterprise.query.filter_by(parentId=enterpriseId).first() is None:
            continue
        elif Enterprise.query.filter_by(parentId=enterpriseId).first().parentId in ids:
            continue
        if Food.query.filter_by(enterpriseId=enterpriseId).all() != []:
            res = Food.query.filter_by(enterpriseId=enterpriseId).update({"enterpriseId": None})
            if not res:
                return fail_api(msg="删除失败")
        r = Enterprise.query.filter_by(enterpriseId=enterpriseId).delete()
        s = Enterprise.query.filter_by(parentId=enterpriseId).delete()
        if not r and not s:
            return fail_api(msg="删除失败")
        db.session.commit()
    return success_api(msg="批量删除成功")
