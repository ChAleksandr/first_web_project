import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Project(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'projects'
    id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(50), unique=True)
    about = sqlalchemy.Column(sqlalchemy.String(), nullable=True)
