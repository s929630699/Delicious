from flask import session, current_app
from flask_login import current_user

from applications.extensions import db
from applications.models import User, user_role


def init_template_directives(app):
    @app.template_global()
    def authorize(power):
        userid = current_user.id
        query = db.session.query(User, user_role).join(
            user_role, User.id == user_role.user_id).filter(User.id == userid).first()
        role_id = query[1].role_id
        if role_id!=1:
            return bool(power in session.get('permissions'))
        else:
            return True
