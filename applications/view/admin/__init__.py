from flask import Flask

from applications.view.admin.activity import activity
from applications.view.admin.admin_log import admin_log
from applications.view.admin.enterprise import enterprise
from applications.view.admin.food import food
from applications.view.admin.foodevaluate import foodevaluate
from applications.view.admin.foodtype import foodtype
from applications.view.admin.index import admin_bp
from applications.view.admin.power import admin_power
from applications.view.admin.role import admin_role
from applications.view.admin.user import admin_user
from applications.view.admin.monitor import admin_monitor_bp


def register_admin_views(app: Flask):
    app.register_blueprint(admin_bp)
    app.register_blueprint(admin_user)
    app.register_blueprint(admin_monitor_bp)
    app.register_blueprint(admin_log)
    app.register_blueprint(admin_power)
    app.register_blueprint(admin_role)
    app.register_blueprint(food)
    app.register_blueprint(foodtype)
    app.register_blueprint(enterprise)
    app.register_blueprint(foodevaluate)
    app.register_blueprint(activity)
