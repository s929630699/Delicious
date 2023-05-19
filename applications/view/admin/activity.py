from datetime import datetime

from flask import Blueprint, render_template, jsonify, request

from applications.common import curd
from applications.common.utils import upload
from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import Activity
from applications.schemas import ActivityOutSchema

activity = Blueprint('activity',__name__,url_prefix='/admin/activity')

@activity.get('/')
@authorize('admin:activity:main')
def main():
    return render_template('admin/activity/main.html')

@activity.get('/data')
@authorize("admin:activity:main", log=True)
def data():
    title=str_escape(request.args.get('title', type=str))
    filters=[]
    if title:
        filters.append(Activity.title.contains(title))
    activities = Activity.query.filter(*filters).layui_paginate()
    return table_api(data=curd.model_to_dicts(schema=ActivityOutSchema, data=activities.items),count=activities.total)


@activity.get('/add')
@authorize("admin:activity:add", log=True)
def add():
    return render_template('admin/activity/add.html')

@activity.post('/save')
@authorize("admin:activity:add", log=True)
def save():
    req = request.get_json(force=True)
    title=str_escape(req.get("title"))
    file=str_escape(req.get("file"))
    image='/_uploads/photos/'+file[file.rfind('\\')+1:]
    contents = str_escape(req.get("contents"))
    addtime = datetime.now()
    hits=0

    activity = Activity(
        title=title,
        image=image,
        contents=contents,
        addtime=addtime,
        hits=hits
    )
    db.session.add(activity)
    db.session.commit()
    return success_api(msg="添加成功")

#   上传接口
@activity.post('/upload')
@authorize("admin:activity:add", log=True)
def upload_api():
    if 'file' in request.files:
        photo = request.files['file']
        mime = request.files['file'].content_type

        file_url = upload.upload_one(photo=photo)
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
@activity.get('/edit/<int:activityId>')
@authorize("admin:activity:edit", log=True)
def edit(activityId):
    activity = Activity.query.filter_by(activityId=activityId).first()
    return render_template('admin/activity/edit.html', activity=activity)


# 更新美食套餐
@activity.put('/update')
@authorize("admin:activity:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    activityId = req_json.get("activityId")
    file = str_escape(req_json.get("file"))
    image = '/_uploads/photos/' + file[file.rfind('\\') + 1:]
    data = {
        "title" :str_escape(req_json.get("title")),
        "image" :image,
        "contents" :str_escape(req_json.get("contents"))
    }
    activity = Activity.query.filter_by(activityId=activityId).update(data)
    db.session.commit()
    if not activity:
        return fail_api(msg="更新失败")
    return success_api(msg="更新成功")

# 删除
@activity.delete('/remove/<int:activityId>')
@authorize("admin:activity:remove", log=True)
def remove(activityId):
    r = Activity.query.filter_by(activityId=activityId).delete()
    db.session.commit()
    if not r:
        return fail_api(msg="删除失败")
    return success_api(msg="删除成功")


# 批量删除
@activity.delete('/batchRemove')
@authorize("admin:activity:remove", log=True)
def batch_remove():
    ids = request.form.getlist('ids[]')
    print(ids)
    for activityId in ids:
        r = Activity.query.filter_by(activityId=activityId).delete()
        db.session.commit()
    return success_api(msg="批量删除成功")