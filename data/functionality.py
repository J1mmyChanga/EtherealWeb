import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Functionality(SqlAlchemyBase):
    __tablename__ = 'functionality'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    functionality = sqlalchemy.Column(sqlalchemy.String)

    #clothes = orm.relationship("Clothes", back_populates='functionalities')