import logging
from urllib.parse import quote_plus as urlquote

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


class BaseConfig:
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 5000

    SUPERADMIN = 'admin'

    SYSTEM_NAME = 'Delicious'

    UPLOADED_PHOTOS_DEST = 'static/upload'
    UPLOADED_FILES_ALLOW = ['gif', 'jpg']
    UPLOADS_AUTOSERVE = True

    # JSON配置
    JSON_AS_ASCII = False

    SECRET_KEY = "Delicious"

    # redis配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # mysql 配置
    MYSQL_USERNAME = "root"
    MYSQL_PASSWORD = "root"
    MYSQL_HOST = "127.0.0.1"
    MYSQL_PORT = 3306
    MYSQL_DATABASE = "deliciousflask"

    # mysql 数据库的配置信息
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USERNAME}:{urlquote(MYSQL_PASSWORD)}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8"

    # 默认日志等级
    LOG_LEVEL = logging.WARN
    #
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USERNAME = '123@qq.com'
    MAIL_PASSWORD = 'XXXXX'  # 生成的授权码
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    # 設置 APSCHEDULER 參數
    SCHEDULER_API_ENABLED = False
    SCHEDULER_JOBSTORES: dict = {
        'default': SQLAlchemyJobStore(
            url=f'mysql+pymysql://{MYSQL_USERNAME}:{urlquote(MYSQL_PASSWORD)}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}')
    }
    SCHEDULER_EXECUTORS: dict = {
        'default': ThreadPoolExecutor(20)
    }
    SCHEDULER_JOB_DEFAULTS: dict = {
        'coalesce': False,
        'max_instances': 3
    }

    # 插件配置，填写插件的文件名名称，默认不启用插件。
    PLUGIN_ENABLE_FOLDERS = []


