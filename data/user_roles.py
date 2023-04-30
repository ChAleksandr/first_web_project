import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash


class UserRoles(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'user_roles'
    id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer(), sqlalchemy.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = sqlalchemy.Column(sqlalchemy.Integer(), sqlalchemy.ForeignKey('roles.id', ondelete='CASCADE'))